from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_service import ask_ai


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class ChatRequest(BaseModel):
    agent_name: str
    payload: dict


@router.post("/execute")
def execute_ai(request: ChatRequest):
    return ask_ai(
        agent_name=request.agent_name,
        payload=request.payload
    )
