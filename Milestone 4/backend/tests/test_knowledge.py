"""
Tests for Knowledge Assistant API
"""
import pytest
from httpx import AsyncClient
from io import BytesIO


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    response = await client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "full_name": "New User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user):
    """Test user login"""
    response = await client.post(
        "/token",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_create_course(client: AsyncClient):
    """Test course creation"""
    response = await client.post(
        "/courses",
        json={
            "code": "CS102",
            "name": "Data Structures",
            "description": "Learn about data structures"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "CS102"


@pytest.mark.asyncio
async def test_list_courses(client: AsyncClient, test_course):
    """Test listing courses"""
    response = await client.get("/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_upload_document(client: AsyncClient, auth_token, test_course):
    """Test document upload"""
    # Create a simple text file
    file_content = b"This is a test document for the course."
    
    response = await client.post(
        "/knowledge/documents",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"file": ("test.txt", BytesIO(file_content), "text/plain")},
        data={"title": "Test Document", "course_id": test_course.id}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Document"
    assert data["course_id"] == test_course.id


@pytest.mark.asyncio
async def test_list_documents(client: AsyncClient, auth_token):
    """Test listing documents"""
    response = await client.get(
        "/knowledge/documents",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient, auth_token, test_course):
    """Test conversation creation"""
    response = await client.post(
        "/knowledge/conversations",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"course_id": test_course.id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["course_id"] == test_course.id
    assert data["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_chat_query(client: AsyncClient, auth_token, test_course):
    """Test chat query"""
    response = await client.post(
        "/knowledge/chat",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "query": "What is Python?",
            "course_id": test_course.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "confidence_score" in data
    assert "should_escalate" in data
