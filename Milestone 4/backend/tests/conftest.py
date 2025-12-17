"""
Pytest Configuration and Fixtures
"""
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from app.main import app
from app.database import Base, get_db
from app.config import settings
from app import crud, schemas

# Test database URL (use same as main for now, or create separate test DB)
TEST_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override database dependency for testing"""
    async with TestAsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Database session for tests"""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """HTTP client for API testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession):
    """Create a test user"""
    user = await crud.create_user(
        db=db_session,
        user=schemas.UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpass123",
            full_name="Test User"
        )
    )
    return user


@pytest.fixture(scope="function")
async def test_course(db_session: AsyncSession):
    """Create a test course"""
    course = await crud.create_course(
        db=db_session,
        course=schemas.CourseCreate(
            code="CS101",
            name="Introduction to Computer Science",
            description="Test course"
        )
    )
    return course


@pytest.fixture(scope="function")
async def auth_token(client: AsyncClient, test_user):
    """Get authentication token"""
    response = await client.post(
        "/token",
        data={"username": test_user.username, "password": "testpass123"}
    )
    return response.json()["access_token"]
