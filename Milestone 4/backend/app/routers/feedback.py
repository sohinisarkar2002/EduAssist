from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import FeedbackCreate, FeedbackResponse, FeedbackTargetType
from app.crud import create_feedback, list_feedback

router = APIRouter()

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(
    inp: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = 1 # TODO: Replace with user auth
):
    return await create_feedback(db, user_id, inp)

@router.get("/", response_model=list[FeedbackResponse])
async def get_feedback(
    target_id: int,
    target_type: FeedbackTargetType,
    db: AsyncSession = Depends(get_db)
):
    return await list_feedback(db, target_id, target_type.value)
