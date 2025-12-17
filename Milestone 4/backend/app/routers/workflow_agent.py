from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import create_workflow_request, get_workflow_request_by_id, list_workflow_requests
from app.services.workflow_agent_service import run_agent_analysis
from app.schemas import WorkflowRequestCreate, WorkflowRequestOut

router = APIRouter()

@router.post("/workflow-requests/", response_model=WorkflowRequestOut)
async def submit_workflow_request(
    req: WorkflowRequestCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    requester_id: int = 1 # Replace with user auth
):
    obj = await create_workflow_request(db, req, requester_id)
    background_tasks.add_task(run_agent_analysis, obj, db)
    return obj

@router.get("/workflow-requests/{id}", response_model=WorkflowRequestOut)
async def get_request(id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_workflow_request_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404)
    return obj

@router.get("/workflow-requests/", response_model=list[WorkflowRequestOut])
async def list_requests(db: AsyncSession = Depends(get_db), requester_id: int = None):
    return await list_workflow_requests(db, requester_id)
