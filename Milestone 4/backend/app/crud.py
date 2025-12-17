"""
Database CRUD operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app.models import SlideDeck, Slide
from app.schemas import SlideDeckStatus
from typing import List, Optional

from . import models, schemas

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User CRUD
async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    """Get user by username"""
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


# Course CRUD
async def create_course(db: AsyncSession, course: schemas.CourseCreate) -> models.Course:
    """Create a new course"""
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


async def get_courses(db: AsyncSession) -> List[models.Course]:
    """Get all courses"""
    result = await db.execute(select(models.Course))
    return result.scalars().all()


# Document CRUD
async def create_document(
    db: AsyncSession,
    document: schemas.DocumentCreate,
    file_path: str,
    file_type: str,
    file_size: int,
    user_id: int
) -> models.Document:
    """Create a new document"""
    db_document = models.Document(
        title=document.title,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        course_id=document.course_id,
        uploaded_by=user_id
    )
    db.add(db_document)
    await db.commit()
    await db.refresh(db_document)
    return db_document


async def update_document_processed(
    db: AsyncSession,
    document_id: int,
    embedding_ids: List[str]
) -> models.Document:
    """Mark document as processed"""
    result = await db.execute(select(models.Document).where(models.Document.id == document_id))
    document = result.scalar_one_or_none()

    if document:
        document.processed = True
        document.embedding_ids = embedding_ids
        await db.commit()
        await db.refresh(document)

    return document


async def get_documents(db: AsyncSession, course_id: Optional[int] = None) -> List[models.Document]:
    """Get documents, optionally filtered by course"""
    query = select(models.Document).where(models.Document.is_deleted == False)
    if course_id:
        query = query.where(models.Document.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()


# Conversation CRUD
async def create_conversation(
    db: AsyncSession,
    course_id: int,
    student_id: int
) -> models.Conversation:
    """Create a new conversation"""
    db_conversation = models.Conversation(
        course_id=course_id,
        student_id=student_id
    )
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)
    return db_conversation


async def get_conversation(db: AsyncSession, conversation_id: int) -> Optional[models.Conversation]:
    """Get conversation with messages"""
    result = await db.execute(
        select(models.Conversation)
        .where(models.Conversation.id == conversation_id)
        .where(models.Conversation.is_deleted == False)
    )
    return result.scalar_one_or_none()


# Message CRUD
async def create_message(
    db: AsyncSession,
    conversation_id: int,
    sender_type: models.SenderType,
    content: str,
    confidence_score: Optional[float] = None,
    sources: Optional[dict] = None
) -> models.Message:
    """Create a new message"""
    db_message = models.Message(
        conversation_id=conversation_id,
        sender_type=sender_type,
        content=content,
        confidence_score=confidence_score,
        sources=sources
    )
    db.add(db_message)

    # Update conversation's last_message_at
    from datetime import datetime
    result = await db.execute(select(models.Conversation).where(models.Conversation.id == conversation_id))
    conversation = result.scalar_one_or_none()
    if conversation:
        conversation.last_message_at = datetime.now()

    await db.commit()
    await db.refresh(db_message)
    return db_message

"""
Study Guide CRUD Operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from . import models, schemas


# Study Guide CRUD
async def create_study_guide(
    db: AsyncSession,
    guide: schemas.StudyGuideCreate,
    video_id: str,
    video_metadata: dict,
    user_id: int
) -> models.StudyGuide:
    """Create a new study guide"""
    db_guide = models.StudyGuide(
        youtube_url=guide.youtube_url,
        video_id=video_id,
        video_title=video_metadata.get('title'),
        video_duration=video_metadata.get('duration'),
        title=guide.title,
        course_id=guide.course_id,
        priority_segments=[seg.model_dump() for seg in guide.priority_segments],
        created_by=user_id,
        status=models.StudyGuideStatus.PROCESSING
    )
    db.add(db_guide)
    await db.commit()
    await db.refresh(db_guide)
    return db_guide


async def update_study_guide_content(
    db: AsyncSession,
    guide_id: int,
    content: str,
    key_topics: List[str],
    status: models.StudyGuideStatus = models.StudyGuideStatus.COMPLETED
) -> models.StudyGuide:
    """Update study guide with generated content"""
    result = await db.execute(
        select(models.StudyGuide).where(models.StudyGuide.id == guide_id)
    )
    guide = result.scalar_one_or_none()

    if guide:
        guide.content = content
        guide.key_topics = key_topics
        guide.status = status
        guide.updated_at = datetime.now()
        await db.commit()
        await db.refresh(guide)

    return guide


async def create_video_segment(
    db: AsyncSession,
    guide_id: int,
    segment_data: dict
) -> models.VideoSegment:
    """Create a video segment"""
    db_segment = models.VideoSegment(
        study_guide_id=guide_id,
        start_time=segment_data['start_time'],
        end_time=segment_data['end_time'],
        transcript=segment_data['transcript'],
        priority=segment_data['priority'],
        summary=segment_data.get('summary'),
        key_points=segment_data.get('key_points')
    )
    db.add(db_segment)
    await db.commit()
    await db.refresh(db_segment)
    return db_segment


async def get_study_guide(
    db: AsyncSession,
    guide_id: int
) -> Optional[models.StudyGuide]:
    """Get study guide by ID"""
    result = await db.execute(
        select(models.StudyGuide)
        .where(models.StudyGuide.id == guide_id)
        .where(models.StudyGuide.is_deleted == False)
    )
    return result.scalar_one_or_none()


async def get_study_guides(
    db: AsyncSession,
    course_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> List[models.StudyGuide]:
    """Get study guides with filters"""
    query = select(models.StudyGuide).where(models.StudyGuide.is_deleted == False)

    if course_id:
        query = query.where(models.StudyGuide.course_id == course_id)
    if user_id:
        query = query.where(models.StudyGuide.created_by == user_id)

    result = await db.execute(query)
    return result.scalars().all()


async def delete_study_guide(
    db: AsyncSession,
    guide_id: int
) -> bool:
    """Soft delete study guide"""
    result = await db.execute(
        select(models.StudyGuide).where(models.StudyGuide.id == guide_id)
    )
    guide = result.scalar_one_or_none()

    if guide:
        guide.is_deleted = True
        guide.deleted_at = datetime.now()
        await db.commit()
        return True

    return False


"""
Assessment CRUD Operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from . import models, schemas


# Assessment CRUD
async def create_assessment(
    db: AsyncSession,
    assessment: schemas.AssessmentCreate,
    user_id: int
) -> models.Assessment:
    """Create a new assessment"""
    db_assessment = models.Assessment(
        title=assessment.title,
        description=assessment.description,
        custom_prompt=assessment.custom_prompt,
        difficulty_level=models.DifficultyLevel(assessment.difficulty_level),
        question_types=[qt.value for qt in assessment.question_types],
        total_questions=assessment.total_questions,
        reference_document_ids=assessment.reference_document_ids,
        duration_minutes=assessment.duration_minutes,
        course_id=assessment.course_id,
        created_by=user_id,
        status=models.AssessmentStatus.GENERATING
    )
    db.add(db_assessment)
    await db.commit()
    await db.refresh(db_assessment)
    return db_assessment


async def update_assessment_completion(
    db: AsyncSession,
    assessment_id: int,
    total_marks: int,
    status: models.AssessmentStatus = models.AssessmentStatus.COMPLETED
) -> models.Assessment:
    """Mark assessment as completed"""
    result = await db.execute(
        select(models.Assessment).where(models.Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()

    if assessment:
        assessment.total_marks = total_marks
        assessment.status = status
        assessment.updated_at = datetime.now()
        await db.commit()
        await db.refresh(assessment)

    return assessment


async def create_question(
    db: AsyncSession,
    assessment_id: int,
    question_data: dict
) -> models.Question:
    """Create a question"""
    db_question = models.Question(
        assessment_id=assessment_id,
        question_type=models.QuestionType(question_data['question_type']),
        question_text=question_data['question_text'],
        options=question_data.get('options'),
        correct_answer=question_data['correct_answer'],
        explanation=question_data.get('explanation'),
        marks=question_data['marks'],
        difficulty=models.DifficultyLevel(question_data.get('difficulty', 'MEDIUM')),
        order=question_data['order']
    )
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)
    return db_question


async def get_assessment(
    db: AsyncSession,
    assessment_id: int,
    include_answers: bool = False
) -> Optional[models.Assessment]:
    """Get assessment by ID"""
    result = await db.execute(
        select(models.Assessment)
        .where(models.Assessment.id == assessment_id)
        .where(models.Assessment.is_deleted == False)
    )
    assessment = result.scalar_one_or_none()

    # If not including answers, remove them from questions
    if assessment and not include_answers:
        for question in assessment.questions:
            question.correct_answer = None
            question.explanation = None

    return assessment


async def get_assessments(
    db: AsyncSession,
    course_id: Optional[int] = None,
    created_by: Optional[int] = None
) -> List[models.Assessment]:
    """Get assessments with filters"""
    query = select(models.Assessment).where(models.Assessment.is_deleted == False)

    if course_id:
        query = query.where(models.Assessment.course_id == course_id)
    if created_by:
        query = query.where(models.Assessment.created_by == created_by)

    result = await db.execute(query)
    return result.scalars().all()


async def delete_assessment(
    db: AsyncSession,
    assessment_id: int
) -> bool:
    """Soft delete assessment"""
    result = await db.execute(
        select(models.Assessment).where(models.Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()

    if assessment:
        assessment.is_deleted = True
        assessment.deleted_at = datetime.now()
        await db.commit()
        return True

    return False


# Assessment Attempt CRUD
async def create_attempt(
    db: AsyncSession,
    assessment_id: int,
    student_id: int,
    max_score: int
) -> models.AssessmentAttempt:
    """Create assessment attempt"""
    db_attempt = models.AssessmentAttempt(
        assessment_id=assessment_id,
        student_id=student_id,
        max_score=max_score
    )
    db.add(db_attempt)
    await db.commit()
    await db.refresh(db_attempt)
    return db_attempt


async def submit_attempt(
    db: AsyncSession,
    attempt_id: int,
    answers: dict,
    score: float,
    time_taken: int
) -> models.AssessmentAttempt:
    """Submit assessment attempt"""
    result = await db.execute(
        select(models.AssessmentAttempt).where(models.AssessmentAttempt.id == attempt_id)
    )
    attempt = result.scalar_one_or_none()

    if attempt:
        attempt.answers = answers
        attempt.score = score
        attempt.percentage = (score / attempt.max_score * 100) if attempt.max_score > 0 else 0
        attempt.submitted_at = datetime.now()
        attempt.time_taken_minutes = time_taken
        await db.commit()
        await db.refresh(attempt)

    return attempt


async def get_student_attempts(
    db: AsyncSession,
    student_id: int,
    assessment_id: Optional[int] = None
) -> List[models.AssessmentAttempt]:
    """Get student's attempts"""
    query = select(models.AssessmentAttempt).where(
        models.AssessmentAttempt.student_id == student_id
    )

    if assessment_id:
        query = query.where(models.AssessmentAttempt.assessment_id == assessment_id)

    result = await db.execute(query)
    return result.scalars().all()

async def get_slide_deck(db: AsyncSession, deck_id: int, owner_id: int) -> Optional[SlideDeck]:
    res = await db.execute(
        select(SlideDeck).where(SlideDeck.id == deck_id, SlideDeck.owner_id == owner_id)
    )
    deck = res.scalar_one_or_none()
    return deck

async def list_slide_decks(db: AsyncSession, owner_id: int, status: Optional[SlideDeckStatus]=None) -> List[SlideDeck]:
    q = select(SlideDeck).where(SlideDeck.owner_id == owner_id)
    if status:
        q = q.where(SlideDeck.status == status)
    res = await db.execute(q.order_by(SlideDeck.created_at.desc()))
    return res.scalars().all()

async def update_slide_content(db: AsyncSession, slide_id: int, owner_id: int, new_content_md: str, new_notes_md: str) -> Optional[Slide]:
    res = await db.execute(
        select(Slide).join(SlideDeck).where(
            Slide.id == slide_id,
            SlideDeck.owner_id == owner_id
        )
    )
    slide = res.scalar_one_or_none()
    if slide:
        slide.content_md = new_content_md
        slide.notes_md = new_notes_md
        await db.commit()
        return slide
    return None

async def create_slide_deck(db: AsyncSession, deck: SlideDeck):
    db.add(deck)
    await db.commit()
    await db.refresh(deck)
    return deck


from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WorkflowRequest
from app.schemas import WorkflowRequestCreate

async def create_workflow_request(db: AsyncSession, req: WorkflowRequestCreate, requester_id: int) -> WorkflowRequest:
    obj = WorkflowRequest(
        title=req.title,
        description=req.description,
        request_type=req.request_type,
        requester_id=requester_id,
        created_at=datetime.utcnow()
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_workflow_request_by_id(db: AsyncSession, request_id: int) -> WorkflowRequest:
    return await db.get(WorkflowRequest, request_id)

async def list_workflow_requests(db: AsyncSession, requester_id: int = None):
    from sqlalchemy import select
    q = select(WorkflowRequest)
    if requester_id:
        q = q.where(WorkflowRequest.requester_id == requester_id)
    res = await db.execute(q.order_by(WorkflowRequest.created_at.desc()))
    return res.scalars().all()


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Feedback
from app.schemas import FeedbackCreate
import datetime
import json

async def create_feedback(db: AsyncSession, user_id: int, inp: FeedbackCreate) -> Feedback:
    fb = Feedback(
        user_id=user_id,
        target_id=inp.target_id,
        target_type=inp.target_type.value,
        rating=inp.rating,
        aspect_ratings=json.dumps(inp.aspect_ratings) if inp.aspect_ratings else None,
        comment=inp.comment,
        created_at=datetime.datetime.utcnow()
    )
    db.add(fb)
    await db.commit()
    await db.refresh(fb)
    return fb

async def list_feedback(
    db: AsyncSession, target_id: int, target_type: str
):
    res = await db.execute(
        select(Feedback).where(
            Feedback.target_id == target_id,
            Feedback.target_type == target_type
        ).order_by(Feedback.created_at.desc())
    )
    return res.scalars().all()

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    """Get user by email"""
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()