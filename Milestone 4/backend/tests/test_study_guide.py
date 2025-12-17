"""
Tests for Study Guide Generator API
tests/test_study_guide.py
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_video_info(client: AsyncClient, auth_token):
    """Test getting YouTube video information"""
    response = await client.get(
        "/study-guides/video-info",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "video_id" in data
    assert "title" in data
    assert "duration" in data
    assert "has_captions" in data


@pytest.mark.asyncio
async def test_get_video_info_invalid_url(client: AsyncClient, auth_token):
    """Test invalid YouTube URL"""
    response = await client.get(
        "/study-guides/video-info",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"url": "https://invalid-url.com"}
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_study_guide(client: AsyncClient, auth_token, test_course):
    """Test creating a study guide"""
    response = await client.post(
        "/study-guides/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course_id": test_course.id,
            "title": "Test Study Guide",
            "priority_segments": [
                {"start": 10, "end": 60, "priority": "high"},
                {"start": 120, "end": 180, "priority": "medium"}
            ]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Study Guide"
    assert data["status"] == "PROCESSING"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_study_guide_no_captions(client: AsyncClient, auth_token, test_course):
    """Test creating study guide for video without captions"""
    # This should fail if video has no captions
    response = await client.post(
        "/study-guides/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "youtube_url": "https://www.youtube.com/watch?v=invalid",
            "course_id": test_course.id,
            "title": "Test",
            "priority_segments": [{"start": 0, "end": 10, "priority": "high"}]
        }
    )

    assert response.status_code in [400, 404]


@pytest.mark.asyncio
async def test_get_study_guide(client: AsyncClient, auth_token, test_course):
    """Test getting study guide by ID"""
    # First create one
    create_response = await client.post(
        "/study-guides/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course_id": test_course.id,
            "title": "Test Guide",
            "priority_segments": [{"start": 10, "end": 60, "priority": "high"}]
        }
    )
    guide_id = create_response.json()["id"]

    # Get it
    response = await client.get(
        f"/study-guides/{guide_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == guide_id
    assert data["title"] == "Test Guide"


@pytest.mark.asyncio
async def test_list_study_guides(client: AsyncClient, auth_token, test_course):
    """Test listing study guides"""
    response = await client.get(
        "/study-guides/",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"course_id": test_course.id}
    )

    assert response.status_code == 200
    data = response.json()
    assert "guides" in data
    assert "total" in data
    assert isinstance(data["guides"], list)


@pytest.mark.asyncio
async def test_delete_study_guide(client: AsyncClient, auth_token, test_course):
    """Test deleting study guide"""
    # Create one
    create_response = await client.post(
        "/study-guides/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course_id": test_course.id,
            "title": "To Delete",
            "priority_segments": [{"start": 0, "end": 30, "priority": "low"}]
        }
    )
    guide_id = create_response.json()["id"]

    # Delete it
    response = await client.delete(
        f"/study-guides/{guide_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_transcript(client: AsyncClient, auth_token):
    """Test getting video transcript"""
    response = await client.get(
        "/study-guides/transcript/dQw4w9WgXcQ",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # May succeed or fail depending on if video has captions
    assert response.status_code in [200, 400]


@pytest.mark.asyncio
async def test_get_transcript_segment(client: AsyncClient, auth_token):
    """Test getting transcript segment"""
    response = await client.get(
        "/study-guides/transcript/dQw4w9WgXcQ",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"start": 10, "end": 60}
    )

    # May succeed or fail depending on captions availability
    if response.status_code == 200:
        data = response.json()
        assert "text" in data


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing without authentication"""
    response = await client.get("/study-guides/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_segment_times(client: AsyncClient, auth_token, test_course):
    """Test creating study guide with invalid segment times"""
    response = await client.post(
        "/study-guides/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course_id": test_course.id,
            "title": "Invalid Segments",
            "priority_segments": [
                {"start": 100, "end": 50, "priority": "high"}  # end < start
            ]
        }
    )

    assert response.status_code == 422  # Validation error
