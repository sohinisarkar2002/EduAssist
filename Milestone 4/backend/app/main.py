"""
EduAssist FastAPI Application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import jwt

from .config import settings
from .database import init_db, get_db
from . import crud, schemas
from .routers import knowledge, study_guide, assessment, slide_deck
from .routers.slide_deck import router as slide_deck_router
from app.routers.workflow_agent import router as workflow_agent_router
from app.routers.feedback import router as feedback_router

# Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting EduAssist API...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down EduAssist API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Teaching Assistant Platform - Knowledge Assistant Feature",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(knowledge.router, prefix="/knowledge-assistant", tags=["Knowledge Assistant"])
app.include_router(study_guide.router, prefix="/study-guides", tags=["Study Guides"])
app.include_router(assessment.router, prefix="/assessments", tags=["Assessments"])
app.include_router(slide_deck_router, prefix="/slide-decks", tags=["Slide Decks"])
app.include_router(workflow_agent_router, prefix="/admin-workflow", tags=["Admin Workflow"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])
from app.routers.auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["Auth"])



# ============ Auth Endpoints ============

def create_access_token(data: dict):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token"""
    user = await crud.get_user_by_username(db, username=form_data.username)

    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    # Check if user exists
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return await crud.create_user(db=db, user=user)


# ============ Course Endpoints ============

@app.post("/courses", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: schemas.CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new course"""
    return await crud.create_course(db=db, course=course)


@app.get("/courses", response_model=list[schemas.CourseResponse])
async def list_courses(db: AsyncSession = Depends(get_db)):
    """List all courses"""
    return await crud.get_courses(db=db)


# ============ Health Check ============

@app.get("/")
async def root():
    """Health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "operational",
            "database": "operational",
            "rag": "operational"
        }
    }
