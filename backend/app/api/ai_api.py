from fastapi import APIRouter
from services.ai_service import ask_ai

from app.ai_agents.orchestrator import AIOrchestrator

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

orchestrator = AIOrchestrator()


@router.post("/chat")
def ai_chat(question: str):
    return ask_ai(question)


@router.post("/workflow")
async def ai_workflow(payload: dict):
    return await orchestrator.run(payload)
