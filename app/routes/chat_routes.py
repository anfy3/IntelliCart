from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest
from app.agents.orchestrator_agent import run_orchestrator

router = APIRouter(prefix="/chat", tags=["Shopping Chatbot"])


@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    result = run_orchestrator(
        user_message=request.message,
        session_id=request.session_id or "default",
        db=db
    )

    return result