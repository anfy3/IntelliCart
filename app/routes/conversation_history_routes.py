from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ConversationHistory
from app.schemas import ConversationHistoryCreate

router = APIRouter(
    prefix="/conversation-history",
    tags=["Conversation History"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_conversation_history(
    history: ConversationHistoryCreate,
    db: Session = Depends(get_db)
):
    new_history = ConversationHistory(**history.dict())

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return new_history


@router.get("/")
def get_conversation_history(db: Session = Depends(get_db)):
    return db.query(ConversationHistory).all()


@router.get("/{history_id}")
def get_conversation_history_by_id(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(ConversationHistory).filter(
        ConversationHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Conversation history not found"
        )

    return history


@router.put("/{history_id}")
def update_conversation_history(
    history_id: int,
    updated_history: ConversationHistoryCreate,
    db: Session = Depends(get_db)
):
    history = db.query(ConversationHistory).filter(
        ConversationHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Conversation history not found"
        )

    for key, value in updated_history.dict().items():
        setattr(history, key, value)

    db.commit()
    db.refresh(history)

    return history


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(ConversationHistory).filter(
        ConversationHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Conversation history not found"
        )

    db.delete(history)
    db.commit()

    return None