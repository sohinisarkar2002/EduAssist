from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.schemas import SlideDeckCreate, SlideDeckOut, SlideOut
from app.crud import get_slide_deck, list_slide_decks, update_slide_content
from app.services.slide_deck_service import create_slide_deck
from app.services.rag_service import extract_text_from_documents  # existing import

router = APIRouter(prefix="/slide-decks", tags=["Slide Decks"])

@router.post("/", response_model=dict)
async def start_slide_deck(
    body: SlideDeckCreate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)  # Uncomment if auth
):
    """
    Generate slide deck from uploaded docs. Returns deck_id (status PENDING/COMPLETE)
    """
    # Example: owner_id=1, but should use current_user.id
    owner_id = 1
    # Presume you have doc text extraction from doc IDs
    ref_texts = await extract_text_from_documents(body.reference_document_ids, db)
    deck_id = await create_slide_deck(db, owner_id, body.title, body.controls, ref_texts)
    return {"deck_id": deck_id}

@router.get("/{deck_id}", response_model=SlideDeckOut)
async def get_deck(
    deck_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user),
):
    owner_id = 1
    deck = await get_slide_deck(db, deck_id, owner_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Slide Deck not found")
    return deck

@router.get("/", response_model=List[SlideDeckOut])
async def list_decks(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    owner_id = 1
    decks = await list_slide_decks(db, owner_id, status)
    return decks

@router.put("/{deck_id}/slide/{slide_id}", response_model=SlideOut)
async def update_slide(
    deck_id: int,
    slide_id: int,
    content_md: str,
    notes_md: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    owner_id = 1
    updated = await update_slide_content(db, slide_id, owner_id, content_md, notes_md)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found or permission denied")
    return updated
