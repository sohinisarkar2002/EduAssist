import asyncio
import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WorkflowRequest, WorkflowStatus
from langchain_google_genai import ChatGoogleGenerativeAI
import langchain
from typing import Optional
from app.config import settings

def build_workflow_agent_prompt(request: WorkflowRequest, requester_history: Optional[str] = None) -> str:
    """
    Prepare a comprehensive prompt for the workflow agent with context and explicit instructions.
    """
    base_prompt = f'''
You are an expert educational admin agent with access to student support policies and historical request data.
Given below is a new admin workflow request. Your tasks:
1. Analyze the request type, description, and any available requester history.
2. Apply policy:
   - If this is an extension, and requester has more than 3 extensions this semester, flag for manual review.
   - If similar requests were approved before and the student history is good, recommend AUTO-APPROVAL.
   - If requester has a negative pattern or the request lacks justification, REJECT.
3. If unsure, summarize reasoning and recommend MANUAL REVIEW.
Return output as JSON: {"decision": "AUTO_APPROVE"|"REJECT"|"MANUAL_REVIEW", "reasoning": string, "policy_check": string}
\nREQUEST DETAILS:\nTitle: {request.title}\nDescription: {request.description}\nType: {request.request_type}\nCreated At: {request.created_at}\nRequester ID: {request.requester_id}
'''
    if requester_history:
        base_prompt += f'\nRequester History:\n{requester_history}\n'
    return base_prompt

async def run_agent_analysis(
    request: WorkflowRequest,
    db: AsyncSession,
    requester_history: Optional[str] = None
):
    """
    Runs LangChain Gemini agent for workflow automation.
    Updates 'agent_decision', 'status', 'agent_reasoning', 'last_run_report' and saves.
    """
    try:
        prompt = build_workflow_agent_prompt(request, requester_history)
        llm = ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL, google_api_key=settings.GEMINI_API_KEY)
        chain = langchain.chains.LLMChain(llm=llm, prompt=prompt)
        loop = asyncio.get_event_loop()
        agent_output = await loop.run_in_executor(None, chain.run, {})

        # Attempt to extract JSON; fallback to text parse
        import json
        agent_json = None
        try:
            agent_json = json.loads(agent_output)
        except Exception:
            agent_json = None
        # Decision logic
        if agent_json and isinstance(agent_json, dict) and 'decision' in agent_json:
            decision = agent_json['decision'].upper()
        else:
            raw = agent_output.upper()
            if 'AUTO-APPROVE' in raw:
                decision = "AUTO_APPROVE"
            elif 'REJECT' in raw:
                decision = "REJECTED"
            else:
                decision = "MANUAL_REVIEW"
        # Map decision to status
        if decision == "AUTO_APPROVE":
            request.agent_decision = "AUTO_APPROVED"
            request.status = WorkflowStatus.AUTO_APPROVED
        elif decision == "REJECTED":
            request.agent_decision = "REJECTED"
            request.status = WorkflowStatus.REJECTED
        else:
            request.agent_decision = "MANUAL_REVIEW"
            request.status = WorkflowStatus.IN_PROGRESS
        # Save reasoning and last_run
        request.agent_reasoning = agent_json["reasoning"] if agent_json and "reasoning" in agent_json else agent_output
        request.last_run_report = {"raw": agent_output, "parsed": agent_json}
        request.resolved_at = datetime.datetime.utcnow()
        await db.commit()
        return request
    except Exception as e:
        logging.exception(f"Agent analysis failed: {e}")
        request.agent_decision = "ERROR"
        request.status = WorkflowStatus.IN_PROGRESS
        request.agent_reasoning = f"Agent error: {e}"
        request.last_run_report = {"error": str(e)}
        await db.commit()
        return request
