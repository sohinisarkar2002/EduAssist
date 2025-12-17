"""
RAG Service with ChromaDB
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict
import PyPDF2
import io
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Document  # Make sure this matches your project

from ..config import settings
from .gemini_client import gemini_client


class RAGService:
    """RAG service for document processing and querying"""

    def __init__(self):
        # Initialize ChromaDB
        self.client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                anonymized_telemetry=False
            )
        )
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    async def process_document(
        self,
        file_content: bytes,
        file_type: str,
        document_id: int,
        course_id: int
    ) -> List[str]:
        """
        Process document and store in vector database
        """
        # Extract text based on file type
        if file_type == "application/pdf":
            text = self._extract_text_from_pdf(file_content)
        elif file_type == "text/plain":
            text = file_content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Split into chunks
        chunks = self._chunk_text(text)

        # Generate embeddings
        embeddings = await gemini_client.generate_embeddings(chunks)

        # Store in ChromaDB
        ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"doc_{document_id}_chunk_{i}"
            ids.append(chunk_id)
            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "document_id": document_id,
                    "course_id": course_id,
                    "chunk_index": i
                }]
            )
        return ids

    async def query(
        self,
        query_text: str,
        course_id: int,
        top_k: int = None
    ) -> List[Dict]:
        """
        Query the knowledge base
        """
        if top_k is None:
            top_k = settings.RAG_TOP_K

        # Generate query embedding
        query_embedding = await gemini_client.generate_embeddings([query_text])

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            where={"course_id": course_id}
        )

        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        return formatted_results

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        pdf_file = io.BytesIO(file_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        chunk_size = settings.RAG_CHUNK_SIZE
        overlap = settings.RAG_CHUNK_OVERLAP
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks


# Singleton instance
rag_service = RAGService()


async def extract_text_from_documents(
    document_ids: List[int], db: AsyncSession
) -> List[str]:
    """
    Given a list of document IDs, returns a list of document texts for further processing.
    """
    result = []
    for doc_id in document_ids:
        doc = await db.get(Document, doc_id)
        if not doc:
            continue
        # Adapt according to your document model!
        if hasattr(doc, "file_path") and doc.file_path:
            # Read file from disk
            with open(doc.file_path, "rb") as f:
                file_content = f.read()
            if doc.file_type == "application/pdf":
                text = rag_service._extract_text_from_pdf(file_content)
            elif doc.file_type == "text/plain":
                text = file_content.decode("utf-8")
            else:
                continue
            result.append(text)
        elif hasattr(doc, "file_content") and doc.file_content:
            # file_content is bytes
            if doc.file_type == "application/pdf":
                text = rag_service._extract_text_from_pdf(doc.file_content)
            elif doc.file_type == "text/plain":
                text = doc.file_content.decode("utf-8")
            else:
                continue
            result.append(text)
    return result
