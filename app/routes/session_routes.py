from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession

from app.database import get_db
from app.models import Session
from app.schemas import SessionCreate

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)

def create_session(
    session: SessionCreate,
    db: DBSession = Depends(get_db)
):
    session_data = session.dict()

    new_session = Session(
        session_code=session_data["session_code"],
        user_preference=session_data.get("user_preference")
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


@router.get("/")
def get_sessions(db: DBSession = Depends(get_db)):
    return db.query(Session).all()


@router.get("/{session_id}")
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    session = db.query(Session).filter(
        Session.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: DBSession = Depends(get_db)
):
    session = db.query(Session).filter(
        Session.id == session_id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return None