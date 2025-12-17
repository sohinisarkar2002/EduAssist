"""
Knowledge Assistant API Endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os
import aiofiles
from datetime import datetime

from ..database import get_db
from ..dependencies import get_current_user, validate_file_upload
from .. import crud, schemas, models
from ..services.rag_service import rag_service
from ..services.gemini_client import gemini_client
from ..config import settings

router = APIRouter(prefix="/knowledge", tags=["Knowledge Assistant"])


# ============ Document Management ============

@router.post("/documents", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    course_id: int = 1,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and process a document for RAG knowledge base
    """
    # Validate file
    validate_file_upload(file)

    # Read file content
    content = await file.read()
    file_size = len(content)

    # Check file size
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )

    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(
        settings.UPLOAD_DIR,
        f"{datetime.now().timestamp()}_{file.filename}"
    )

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)

    # Create document record
    document = await crud.create_document(
        db=db,
        document=schemas.DocumentCreate(
            title=title or file.filename,
            course_id=course_id
        ),
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size,
        user_id=current_user.id
    )

    # Process document with RAG
    try:
        embedding_ids = await rag_service.process_document(
            file_content=content,
            file_type=file.content_type,
            document_id=document.id,
            course_id=course_id
        )

        # Update document as processed
        document = await crud.update_document_processed(
            db=db,
            document_id=document.id,
            embedding_ids=embedding_ids
        )
    except Exception as e:
        print(f"Error processing document: {e}")
        # Document created but not processed

    return document


@router.get("/documents", response_model=List[schemas.DocumentResponse])
async def list_documents(
    course_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """List all documents"""
    documents = await crud.get_documents(db=db, course_id=course_id)
    return documents


# ============ Conversation Management ============

@router.post("/conversations", response_model=schemas.ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: schemas.ConversationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new conversation"""
    db_conversation = await crud.create_conversation(
        db=db,
        course_id=conversation.course_id,
        student_id=current_user.id
    )
    return db_conversation


@router.get("/conversations/{conversation_id}", response_model=schemas.ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get conversation with messages"""
    conversation = await crud.get_conversation(db=db, conversation_id=conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return conversation


# ============ Chat / Query ============

@router.post("/chat", response_model=schemas.ChatQueryResponse)
async def chat_query(
    query: schemas.ChatQueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Process a chat query using RAG

    Steps:
    1. Query knowledge base for relevant context
    2. Generate response with Gemini
    3. Save message to conversation
    4. Return response with confidence score
    """
    # Get or create conversation
    if query.conversation_id:
        conversation = await crud.get_conversation(db=db, conversation_id=query.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = await crud.create_conversation(
            db=db,
            course_id=query.course_id,
            student_id=current_user.id
        )

    # Save user message
    await crud.create_message(
        db=db,
        conversation_id=conversation.id,
        sender_type=models.SenderType.STUDENT,
        content=query.query
    )

    # Query RAG knowledge base
    relevant_docs = await rag_service.query(
        query_text=query.query,
        course_id=query.course_id,
        top_k=settings.RAG_TOP_K
    )

    # Build context from relevant documents
    context = "\n\n".join([doc["text"] for doc in relevant_docs[:3]])

    # Calculate confidence (average similarity from top results)
    if relevant_docs:
        # Convert distance to similarity (assuming cosine distance)
        confidences = [1 - doc["distance"] for doc in relevant_docs if doc["distance"] is not None]
        confidence_score = sum(confidences) / len(confidences) if confidences else 0.0
    else:
        confidence_score = 0.0

    # Generate response with Gemini
    system_instruction = """You are an educational AI assistant. Answer the student's question based on the provided context from course materials. 
If the context doesn't contain enough information, say so clearly. Always be helpful and educational."""

    prompt = f"""Context from course materials:
{context}

Student Question: {query.query}

Please provide a clear, educational answer based on the context above."""

    try:
        ai_response = await gemini_client.generate_completion(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=0.7
        )
    except Exception as e:
        ai_response = f"I apologize, but I encountered an error processing your question. Please try again or contact your TA."
        confidence_score = 0.0

    # Save AI response
    ai_message = await crud.create_message(
        db=db,
        conversation_id=conversation.id,
        sender_type=models.SenderType.AI,
        content=ai_response,
        confidence_score=confidence_score,
        sources={"documents": [doc["metadata"] for doc in relevant_docs[:3]]}
    )

    # Determine if should escalate
    should_escalate = confidence_score < settings.RAG_CONFIDENCE_THRESHOLD

    return schemas.ChatQueryResponse(
        message=ai_message,
        should_escalate=should_escalate,
        confidence_score=confidence_score
    )
