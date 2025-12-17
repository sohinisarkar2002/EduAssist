import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_slide_deck(client: AsyncClient):
    payload = {
        "title": "Sample Deck",
        "controls": {"num_slides": 5, "desired_depth": "summary"},
        "reference_document_ids": []
    }
    response = await client.post("/slide-decks/", json=payload)
    assert response.status_code == 200
    assert "deck_id" in response.json()

@pytest.mark.asyncio
async def test_get_slide_deck(client: AsyncClient):
    # First, create a deck
    create = await client.post("/slide-decks/", json={
        "title": "DeckFetch",
        "controls": {"num_slides": 3, "desired_depth": "summary"},
        "reference_document_ids": []
    })
    deck_id = create.json()["deck_id"]
    res = await client.get(f"/slide-decks/{deck_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "DeckFetch"
