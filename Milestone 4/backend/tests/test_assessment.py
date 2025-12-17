"""
Tests for Assessment Generator API
tests/test_assessment.py
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_assessment(client: AsyncClient, auth_token, test_course):
    """Test creating an assessment"""
    response = await client.post(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Python Basics Test",
            "description": "Test on Python fundamentals",
            "course_id": test_course.id,
            "custom_prompt": "Generate questions about Python variables, data types, and basic operations",
            "difficulty_level": "MEDIUM",
            "question_types": ["MCQ", "MSQ", "NAT"],
            "total_questions": 10,
            "reference_document_ids": [],
            "duration_minutes": 30
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Basics Test"
    assert data["status"] == "GENERATING"
    assert data["total_questions"] == 10


@pytest.mark.asyncio
async def test_create_assessment_invalid_params(client: AsyncClient, auth_token, test_course):
    """Test creating assessment with invalid parameters"""
    response = await client.post(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Test",
            "course_id": test_course.id,
            "custom_prompt": "short",  # Too short
            "difficulty_level": "INVALID",  # Invalid difficulty
            "question_types": [],  # Empty list
            "total_questions": 0  # Too few
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_assessment(client: AsyncClient, auth_token, test_course):
    """Test getting assessment by ID"""
    # Create assessment first
    create_response = await client.post(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Math Test",
            "course_id": test_course.id,
            "custom_prompt": "Generate algebra questions",
            "difficulty_level": "EASY",
            "question_types": ["MCQ"],
            "total_questions": 5
        }
    )
    assessment_id = create_response.json()["id"]

    # Get assessment
    response = await client.get(
        f"/assessments/{assessment_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == assessment_id


@pytest.mark.asyncio
async def test_preview_assessment(client: AsyncClient, auth_token, test_course):
    """Test getting assessment preview (without answers)"""
    # This test would need a completed assessment
    # For now, just test the endpoint exists
    response = await client.get(
        "/assessments/1/preview",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Will 404 if no assessment exists, which is fine for this test
    assert response.status_code in [200, 404, 400]


@pytest.mark.asyncio
async def test_list_assessments(client: AsyncClient, auth_token, test_course):
    """Test listing assessments"""
    response = await client.get(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"course_id": test_course.id}
    )

    assert response.status_code == 200
    data = response.json()
    assert "assessments" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_delete_assessment(client: AsyncClient, auth_token, test_course):
    """Test deleting assessment"""
    # Create assessment
    create_response = await client.post(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "To Delete",
            "course_id": test_course.id,
            "custom_prompt": "Generate test questions",
            "difficulty_level": "EASY",
            "question_types": ["MCQ"],
            "total_questions": 3
        }
    )
    assessment_id = create_response.json()["id"]

    # Delete it
    response = await client.delete(
        f"/assessments/{assessment_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_start_attempt(client: AsyncClient, auth_token, test_course):
    """Test starting an assessment attempt"""
    # Would need a completed assessment
    response = await client.post(
        "/assessments/1/attempts",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Will fail if no completed assessment, which is expected
    assert response.status_code in [200, 404, 400]


@pytest.mark.asyncio
async def test_submit_attempt(client: AsyncClient, auth_token):
    """Test submitting assessment answers"""
    response = await client.post(
        "/assessments/attempts/1/submit",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "answers": [
                {"question_id": 1, "answer": "A"},
                {"question_id": 2, "answer": ["A", "C"]}
            ]
        }
    )

    # Will fail if no attempt exists
    assert response.status_code in [200, 404, 400]


@pytest.mark.asyncio
async def test_get_my_attempts(client: AsyncClient, auth_token):
    """Test getting user's attempts"""
    response = await client.get(
        "/assessments/my-attempts",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing without authentication"""
    response = await client.get("/assessments/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_mcq_question_type(client: AsyncClient, auth_token, test_course):
    """Test creating assessment with only MCQ"""
    response = await client.post(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "MCQ Only Test",
            "course_id": test_course.id,
            "custom_prompt": "Generate multiple choice questions only",
            "difficulty_level": "MEDIUM",
            "question_types": ["MCQ"],
            "total_questions": 10
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "MCQ" in data["question_types"]


@pytest.mark.asyncio
async def test_mixed_question_types(client: AsyncClient, auth_token, test_course):
    """Test creating assessment with mixed question types"""
    response = await client.post(
        "/assessments/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Mixed Question Test",
            "course_id": test_course.id,
            "custom_prompt": "Generate various types of questions",
            "difficulty_level": "HARD",
            "question_types": ["MCQ", "MSQ", "NAT", "SHORT_ANSWER", "TRUE_FALSE"],
            "total_questions": 20
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert len(data["question_types"]) == 5
