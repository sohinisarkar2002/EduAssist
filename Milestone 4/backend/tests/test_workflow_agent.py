import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_submit_workflow(client: AsyncClient):
    payload = {
        "title": "Extension Request for Assignment 2",
        "description": "My laptop failed the night before deadline.",
        "request_type": "extension"
    }
    res = await client.post("/admin-workflow/workflow-requests/", json=payload)
    assert res.status_code == 200
    assert res.json()["title"] == "Extension Request for Assignment 2"
