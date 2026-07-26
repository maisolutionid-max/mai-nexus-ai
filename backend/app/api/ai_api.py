from fastapi import APIRouter

from services.ai_service import ask_ai

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/chat")
def ai_chat(
    question: str
):

    return ask_ai(question)
