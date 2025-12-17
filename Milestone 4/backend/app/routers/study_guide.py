"""
Study Guide Generator API
app/routers/study_guide.py
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..dependencies import get_current_user
from .. import crud, schemas, models
from ..services.youtube_service import youtube_service
from ..services.study_guide_service import study_guide_service

router = APIRouter(prefix="/study-guides", tags=["Study Guide Generator"])


# ============ Video Information ============

@router.get("/video-info")
async def get_video_info(
    url: str,
    current_user: models.User = Depends(get_current_user)
):
    """
    Get YouTube video information

    Check if video has captions and get metadata before creating study guide
    """
    try:
        # Extract video ID
        video_id = youtube_service.extract_video_id(url)

        # Get metadata
        metadata = youtube_service.get_video_metadata(url)

        # Check captions
        has_captions = youtube_service.check_captions_available(video_id)

        return {
            "video_id": video_id,
            "title": metadata['title'],
            "duration": metadata['duration'],
            "thumbnail_url": metadata['thumbnail_url'],
            "has_captions": has_captions
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error getting video info: {str(e)}"
        )


# ============ Study Guide Generation ============

async def process_study_guide_generation(
    guide_id: int,
    video_id: str,
    priority_segments: List[dict],
    title: str,
    db: AsyncSession
):
    """Background task to generate study guide"""
    try:
        # Get transcript
        transcript = youtube_service.get_transcript(video_id)

        # Generate study guide
        result = await study_guide_service.generate_study_guide(
            video_id=video_id,
            transcript=transcript,
            priority_segments=priority_segments,
            title=title
        )

        # Update study guide with content
        await crud.update_study_guide_content(
            db=db,
            guide_id=guide_id,
            content=result['content'],
            key_topics=result['key_topics'],
            status=models.StudyGuideStatus.COMPLETED
        )

        # Save segments
        for segment_data in result['segments']:
            await crud.create_video_segment(
                db=db,
                guide_id=guide_id,
                segment_data=segment_data
            )

        print(f"✅ Study guide {guide_id} generated successfully")

    except Exception as e:
        print(f"❌ Error generating study guide {guide_id}: {e}")

        # Update status to failed
        await crud.update_study_guide_content(
            db=db,
            guide_id=guide_id,
            content=f"Error: {str(e)}",
            key_topics=[],
            status=models.StudyGuideStatus.FAILED
        )


@router.post("/", response_model=schemas.StudyGuideResponse, status_code=status.HTTP_201_CREATED)
async def create_study_guide(
    guide: schemas.StudyGuideCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a study guide from YouTube video

    Steps:
    1. Validate YouTube URL and get video ID
    2. Get video metadata
    3. Create study guide record (PROCESSING status)
    4. Generate content in background (async)
    5. Return study guide ID immediately

    The client should poll /study-guides/{id} to check status
    """
    try:
        # Extract video ID
        video_id = youtube_service.extract_video_id(guide.youtube_url)

        # Get video metadata
        metadata = youtube_service.get_video_metadata(guide.youtube_url)

        # Check captions available
        if not youtube_service.check_captions_available(video_id):
            raise HTTPException(
                status_code=400,
                detail="Video does not have captions available"
            )

        # Create study guide record
        db_guide = await crud.create_study_guide(
            db=db,
            guide=guide,
            video_id=video_id,
            video_metadata=metadata,
            user_id=current_user.id
        )

        # Convert priority segments to dict
        priority_segments_dict = [
            {"start": seg.start, "end": seg.end, "priority": seg.priority.value}
            for seg in guide.priority_segments
        ]

        # Start background generation
        background_tasks.add_task(
            process_study_guide_generation,
            guide_id=db_guide.id,
            video_id=video_id,
            priority_segments=priority_segments_dict,
            title=guide.title,
            db=db
        )

        return db_guide

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating study guide: {str(e)}"
        )


@router.get("/{guide_id}", response_model=schemas.StudyGuideResponse)
async def get_study_guide(
    guide_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get study guide by ID"""
    guide = await crud.get_study_guide(db=db, guide_id=guide_id)

    if not guide:
        raise HTTPException(status_code=404, detail="Study guide not found")

    # Check authorization
    if guide.created_by != current_user.id and not current_user.is_student:
        raise HTTPException(status_code=403, detail="Not authorized")

    return guide


@router.get("/", response_model=schemas.StudyGuideListResponse)
async def list_study_guides(
    course_id: int = None,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List study guides"""
    # Students can only see their own
    user_id = current_user.id if current_user.is_student else None

    guides = await crud.get_study_guides(
        db=db,
        course_id=course_id,
        user_id=user_id
    )

    return {
        "guides": guides,
        "total": len(guides)
    }


@router.delete("/{guide_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_study_guide(
    guide_id: int,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete study guide"""
    guide = await crud.get_study_guide(db=db, guide_id=guide_id)

    if not guide:
        raise HTTPException(status_code=404, detail="Study guide not found")

    # Check authorization
    if guide.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await crud.delete_study_guide(db=db, guide_id=guide_id)
    return None


# ============ Get Transcript for Preview ============

@router.get("/transcript/{video_id}")
async def get_video_transcript(
    video_id: str,
    start: int = 0,
    end: int = None,
    current_user: models.User = Depends(get_current_user)
):
    """
    Get video transcript for preview

    Used by frontend to show transcript before creating study guide
    """
    try:
        transcript = youtube_service.get_transcript(video_id)

        if end:
            # Extract segment
            text = youtube_service.extract_segment_transcript(
                transcript, start, end
            )
            return {"text": text, "segments": transcript[start:end]}

        return {"segments": transcript}

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error getting transcript: {str(e)}"
        )
