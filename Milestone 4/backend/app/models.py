"""
SQLAlchemy Models for Knowledge Assistant
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .database import Base


# Enums
class ConversationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"


class SenderType(str, enum.Enum):
    STUDENT = "STUDENT"
    AI = "AI"
    TA = "TA"


# Models
class User(Base):
    """User model (simplified)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    password_reset_token = Column(String, nullable=True)
    password_reset_expiry = Column(DateTime, nullable=True)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_student = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    documents = relationship("Document", back_populates="uploader")
    conversations = relationship("Conversation", back_populates="student")


class Course(Base):
    """Course model"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    documents = relationship("Document", back_populates="course")
    conversations = relationship("Conversation", back_populates="course")


class Document(Base):
    """Document uploaded for RAG knowledge base"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)

    # Processing status
    processed = Column(Boolean, default=False)
    embedding_ids = Column(JSON, nullable=True)

    # Foreign keys
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    course = relationship("Course", back_populates="documents")
    uploader = relationship("User", back_populates="documents")


class Conversation(Base):
    """Conversation between student and AI assistant"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    # Status
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)

    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)

    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    student = relationship("User", back_populates="conversations")
    course = relationship("Course", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Individual message in a conversation"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    # Content
    sender_type = Column(Enum(SenderType), nullable=False)
    content = Column(Text, nullable=False)

    # AI response metadata
    confidence_score = Column(Float, nullable=True)
    sources = Column(JSON, nullable=True)

    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

class StudyGuideStatus(str, enum.Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class StudyGuide(Base):
    """Study guide generated from YouTube video"""
    __tablename__ = "study_guides"

    id = Column(Integer, primary_key=True, index=True)

    # YouTube video info
    youtube_url = Column(String(500), nullable=False)
    video_id = Column(String(50), nullable=False)
    video_title = Column(String(500))
    video_duration = Column(Integer)  # in seconds

    # Priority segments (user-selected important parts)
    priority_segments = Column(JSON, nullable=False)
    # Format: [{"start": 120, "end": 180, "priority": "high"}]

    # Generated content
    title = Column(String(255), nullable=False)
    content = Column(Text)  # Markdown formatted study guide
    key_topics = Column(JSON)  # List of key topics extracted

    # Processing
    status = Column(Enum(StudyGuideStatus), default=StudyGuideStatus.PROCESSING)

    # Foreign keys
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    course = relationship("Course", backref="study_guides")
    creator = relationship("User", backref="study_guides")


class VideoSegment(Base):
    """Individual video segment with transcript"""
    __tablename__ = "video_segments"

    id = Column(Integer, primary_key=True, index=True)
    study_guide_id = Column(Integer, ForeignKey("study_guides.id"), nullable=False)

    # Segment info
    start_time = Column(Integer, nullable=False)  # seconds
    end_time = Column(Integer, nullable=False)  # seconds
    transcript = Column(Text, nullable=False)

    # Priority level (set by user)
    priority = Column(String(20), default="medium")  # high, medium, low

    # Generated summary
    summary = Column(Text)
    key_points = Column(JSON)  # List of key points

    # Relationships
    study_guide = relationship("StudyGuide", backref="segments")

class QuestionType(str, enum.Enum):
    MCQ = "MCQ"  # Multiple Choice - Single Answer
    MSQ = "MSQ"  # Multiple Select - Multiple Answers
    NAT = "NAT"  # Numerical Answer Type
    SHORT_ANSWER = "SHORT_ANSWER"
    TRUE_FALSE = "TRUE_FALSE"


class DifficultyLevel(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class AssessmentStatus(str, enum.Enum):
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Assessment(Base):
    """AI-generated assessment/quiz"""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    # Basic info
    title = Column(String(255), nullable=False)
    description = Column(Text)

    # Generation parameters
    custom_prompt = Column(Text)  # User's custom instructions
    difficulty_level = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    question_types = Column(JSON)  # List of question types to generate
    total_questions = Column(Integer, default=10)

    # Status
    status = Column(Enum(AssessmentStatus), default=AssessmentStatus.GENERATING)

    # Reference materials (uploaded PDFs/docs)
    reference_document_ids = Column(JSON)  # List of document IDs used

    # Metadata
    total_marks = Column(Integer)
    duration_minutes = Column(Integer, nullable=True)  # Suggested time

    # Foreign keys
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    course = relationship("Course", backref="assessments")
    creator = relationship("User", backref="created_assessments")
    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan")


class Question(Base):
    """Individual question in an assessment"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)

    # Question content
    question_type = Column(Enum(QuestionType), nullable=False)
    question_text = Column(Text, nullable=False)

    # For MCQ/MSQ: List of options
    options = Column(JSON)  # ["Option A", "Option B", "Option C", "Option D"]

    # Correct answer(s)
    correct_answer = Column(JSON)  # MCQ: ["A"], MSQ: ["A", "C"], NAT: "42.5", SHORT: "text"

    # Additional info
    explanation = Column(Text)  # Why this is the correct answer
    marks = Column(Integer, default=1)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)

    # Question order
    order = Column(Integer)

    # Relationships
    assessment = relationship("Assessment", back_populates="questions")


class AssessmentAttempt(Base):
    """Student's attempt at an assessment"""
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Submission
    answers = Column(JSON)  # {question_id: answer}
    score = Column(Float, nullable=True)
    max_score = Column(Integer)
    percentage = Column(Float, nullable=True)

    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    time_taken_minutes = Column(Integer, nullable=True)

    # Relationships
    assessment = relationship("Assessment")
    student = relationship("User")

class SlideDeckStatus(str, enum.Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class SlideDeck(Base):
    __tablename__ = "slide_decks"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    status = Column(Enum(SlideDeckStatus), default=SlideDeckStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    num_slides = Column(Integer)
    desired_depth = Column(String)
    reference_document_ids = Column(JSON, nullable=True)  # [int]
    slides = relationship("Slide", back_populates="slide_deck")

class Slide(Base):
    __tablename__ = "slides"
    id = Column(Integer, primary_key=True, index=True)
    slide_deck_id = Column(Integer, ForeignKey("slide_decks.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    content_md = Column(Text)  # Markdown for slide
    notes_md = Column(Text)    # Markdown for speaker notes
    image_url = Column(String, nullable=True)
    position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    slide_deck = relationship("SlideDeck", back_populates="slides")

class WorkflowStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"
    AUTO_APPROVED = "AUTO_APPROVED"

class WorkflowRequest(Base):
    __tablename__ = "workflow_requests"
    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    request_type = Column(String, nullable=False)  # extension, objection, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.PENDING)
    agent_decision = Column(String, nullable=True)
    admin_decision = Column(String, nullable=True)
    agent_reasoning = Column(Text, nullable=True)
    last_run_report = Column(JSON, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

import enum
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import datetime

class FeedbackTargetType(str, enum.Enum):
    ASSESSMENT = "assessment"
    STUDY_GUIDE = "study_guide"
    SLIDE_DECK = "slide_deck"

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    target_id = Column(Integer, nullable=False)  # assessment_id, slide_deck_id or study_guide_id
    target_type = Column(Enum(FeedbackTargetType), nullable=False)
    rating = Column(Float, nullable=False)  # 1–5 scale
    aspect_ratings = Column(Text, nullable=True)  # JSON string: {"design":4,"content":5,...}
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)