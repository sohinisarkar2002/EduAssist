from app.schemas import SlideDeckControls, SlideCreate
from typing import List
from app.services.gemini_client import get_gemini_content
from app.services.rag_service import extract_text_from_documents

async def generate_slides_with_gemini(
    title: str,
    controls: SlideDeckControls,
    reference_text: str
) -> List[SlideCreate]:
    """
    Call Gemini to generate the slide breakdown. One prompt for all slides.
    """
    prompt = (
        f"""
        You are an expert lecture material summarizer.
        Given the following material, generate {controls.num_slides} slides for a presentation titled '{title}'.
        Each slide should have:
        - A short slide title
        - Slide content as markdown (concise bullets/phrases with NO paragraph prose)
        - Speaker notes (1-2 sentences explanation as markdown)
        - Optionally, suggest an illustrative image URL or description (where relevant)
        Aim for {controls.desired_depth} level of detail.
        Output:
        - For each slide, a dict: {{'title':..., 'content_md':..., 'notes_md':..., 'image_url':...}}
        Only output JSON list, no commentary.
        -----
        MATERIAL TO SUMMARIZE:
        {reference_text}
        """
    )
    slide_json = await get_gemini_content(prompt, response_format="json")  # List[dict]
    slides = [SlideCreate(**slide) for slide in slide_json]
    return slides

async def create_slide_deck(
    db,
    owner_id: int,
    title: str,
    controls: SlideDeckControls,
    reference_doc_texts: List[str],
) -> int:
    # Combine docs
    ref_text = "\n---\n".join(reference_doc_texts)
    slides = await generate_slides_with_gemini(title, controls, ref_text)
    # Create and return slide deck and slides
    from app.models import SlideDeck, Slide, SlideDeckStatus
    deck = SlideDeck(
        owner_id=owner_id, title=title, status=SlideDeckStatus.COMPLETE,  # For demo; could use background job
        num_slides=controls.num_slides, desired_depth=controls.desired_depth
    )
    db.add(deck)
    await db.flush()
    for idx, slide in enumerate(slides):
        db.add(Slide(
            slide_deck_id=deck.id,
            title=slide.title,
            content_md=slide.content_md,
            notes_md=slide.notes_md,
            image_url=slide.image_url,
            position=idx
        ))
    await db.commit()
    return deck.id
