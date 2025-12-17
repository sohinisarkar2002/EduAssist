"""
Pydantic Schemas for Knowledge Assistant
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict, conint
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
class ConversationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"


class SenderType(str, Enum):
    STUDENT = "STUDENT"
    AI = "AI"
    TA = "TA"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_student: bool
    created_at: datetime


# Document Schemas
class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    course_id: int


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    file_path: str
    file_type: str
    file_size: int
    processed: bool
    course_id: int
    uploaded_by: int
    uploaded_at: datetime


# Conversation Schemas
class ConversationCreate(BaseModel):
    course_id: int


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    sender_type: SenderType
    content: str
    confidence_score: Optional[float] = None
    sources: Optional[dict] = None
    timestamp: datetime


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    course_id: int
    status: ConversationStatus
    started_at: datetime
    last_message_at: Optional[datetime] = None
    messages: List[MessageResponse] = []


# Message Schemas
class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


# Chat Query
class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)
    course_id: int
    conversation_id: Optional[int] = None


class ChatQueryResponse(BaseModel):
    message: MessageResponse
    should_escalate: bool
    confidence_score: float


# Course Schemas
class CourseCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    description: Optional[str] = None
    created_at: datetime


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

"""
Study Guide Generator Schemas
"""
from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum


# Enums
class StudyGuideStatus(str, Enum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# Request/Response Models
class PrioritySegment(BaseModel):
    """User-selected important segment"""
    start: int = Field(..., ge=0, description="Start time in seconds")
    end: int = Field(..., gt=0, description="End time in seconds")
    priority: Priority = Priority.MEDIUM


class StudyGuideCreate(BaseModel):
    """Request to create study guide from YouTube"""
    youtube_url: str = Field(..., min_length=1)
    course_id: int
    title: str = Field(..., min_length=1, max_length=255)
    priority_segments: List[PrioritySegment] = Field(..., min_items=1)


class VideoSegmentResponse(BaseModel):
    """Video segment with transcript"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    start_time: int
    end_time: int
    transcript: str
    priority: str
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None


class StudyGuideResponse(BaseModel):
    """Study guide response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    youtube_url: str
    video_id: str
    video_title: Optional[str] = None
    video_duration: Optional[int] = None
    title: str
    content: Optional[str] = None
    key_topics: Optional[List[str]] = None
    status: StudyGuideStatus
    course_id: int
    created_by: int
    created_at: datetime
    segments: List[VideoSegmentResponse] = []


class StudyGuideListResponse(BaseModel):
    """List of study guides"""
    guides: List[StudyGuideResponse]
    total: int


class VideoInfoResponse(BaseModel):
    """YouTube video metadata"""
    video_id: str
    title: str
    duration: int  # seconds
    thumbnail_url: str
    has_captions: bool


"""
Assessment Generator Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class QuestionType(str, Enum):
    MCQ = "MCQ"
    MSQ = "MSQ"
    NAT = "NAT"
    SHORT_ANSWER = "SHORT_ANSWER"
    TRUE_FALSE = "TRUE_FALSE"


class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class AssessmentStatus(str, Enum):
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# Request Models
class AssessmentCreate(BaseModel):
    """Request to create assessment"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    course_id: int

    # Generation parameters
    custom_prompt: str = Field(..., min_length=10, description="Instructions for question generation")
    difficulty_level: DifficultyLevel = DifficultyLevel.MEDIUM
    question_types: List[QuestionType] = Field(..., min_items=1)
    total_questions: int = Field(..., ge=1, le=100)

    # Reference materials
    reference_document_ids: List[int] = Field(default_factory=list, description="Document IDs to use as reference")

    # Optional
    duration_minutes: Optional[int] = Field(None, ge=5, le=600)


class QuestionResponse(BaseModel):
    """Question response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    assessment_id: int
    question_type: QuestionType
    question_text: str
    options: Optional[List[str]] = None
    correct_answer: Any  # Can be list, string, or number
    explanation: Optional[str] = None
    marks: int
    difficulty: DifficultyLevel
    order: int


class AssessmentResponse(BaseModel):
    """Assessment response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    custom_prompt: str
    difficulty_level: DifficultyLevel
    question_types: List[str]
    total_questions: int
    status: AssessmentStatus
    total_marks: Optional[int] = None
    duration_minutes: Optional[int] = None
    course_id: int
    created_by: int
    created_at: datetime
    questions: List[QuestionResponse] = []


class AssessmentListResponse(BaseModel):
    """List of assessments"""
    assessments: List[AssessmentResponse]
    total: int


# Student attempt
class AnswerSubmission(BaseModel):
    """Student's answer to a question"""
    question_id: int
    answer: Any  # Can be string, list, or number


class AssessmentSubmit(BaseModel):
    """Submit assessment answers"""
    answers: List[AnswerSubmission]


class AssessmentAttemptResponse(BaseModel):
    """Assessment attempt result"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    assessment_id: int
    student_id: int
    score: Optional[float] = None
    max_score: int
    percentage: Optional[float] = None
    started_at: datetime
    submitted_at: Optional[datetime] = None
    time_taken_minutes: Optional[int] = None


# For preview (no answers)
class QuestionPreview(BaseModel):
    """Question without correct answer (for students)"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_type: QuestionType
    question_text: str
    options: Optional[List[str]] = None
    marks: int
    order: int


class AssessmentPreview(BaseModel):
    """Assessment for students (no answers)"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    total_questions: int
    total_marks: int
    duration_minutes: Optional[int] = None
    questions: List[QuestionPreview] = []

class SlideDeckStatus(str, Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class SlideDeckControls(BaseModel):
    num_slides: conint(ge=3, le=30) = 10
    desired_depth: str = Field(default="summary", description="summary, normal, in-depth")

class SlideCreate(BaseModel):
    title: str
    content_md: str
    notes_md: Optional[str] = None
    image_url: Optional[str] = None
    position: int

class SlideOut(SlideCreate):
    id: int

class SlideDeckCreate(BaseModel):
    title: str
    controls: SlideDeckControls
    reference_document_ids: Optional[List[int]] = []

class SlideDeckOut(BaseModel):
    id: int
    title: str
    status: SlideDeckStatus
    controls: SlideDeckControls
    slides: List[SlideOut] = []
    created_at: str

    class Config:
        orm_mode = True

class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"
    AUTO_APPROVED = "AUTO_APPROVED"

class WorkflowRequestCreate(BaseModel):
    title: str
    description: str
    request_type: str

class WorkflowRequestOut(BaseModel):
    id: int
    title: str
    description: str
    request_type: str
    status: WorkflowStatus
    agent_decision: Optional[str] = None
    admin_decision: Optional[str] = None
    agent_reasoning: Optional[str] = None
    last_run_report: Optional[dict] = None
    created_at: str
    resolved_at: Optional[str]
    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional, Dict
import enum

class FeedbackTargetType(str, enum.Enum):
    assessment = "assessment"
    study_guide = "study_guide"
    slide_deck = "slide_deck"

class FeedbackCreate(BaseModel):
    target_id: int
    target_type: FeedbackTargetType
    rating: float = Field(ge=1, le=5)
    aspect_ratings: Optional[Dict[str, float]] = None  # {"difficulty":3, ...}
    comment: Optional[str] = None

class FeedbackResponse(FeedbackCreate):
    id: int
    user_id: int
    created_at: str
    class Config:
        from_attributes = True