from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SearchHistory
from app.schemas import SearchHistoryCreate

router = APIRouter(
    prefix="/search-history",
    tags=["Search History"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_search_history(
    history: SearchHistoryCreate,
    db: Session = Depends(get_db)
):
    new_history = SearchHistory(**history.dict())

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return new_history


@router.get("/")
def get_search_history(db: Session = Depends(get_db)):
    return db.query(SearchHistory).all()


@router.get("/{history_id}")
def get_search_history_by_id(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(SearchHistory).filter(
        SearchHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Search history not found"
        )

    return history


@router.put("/{history_id}")
def update_search_history(
    history_id: int,
    updated_history: SearchHistoryCreate,
    db: Session = Depends(get_db)
):
    history = db.query(SearchHistory).filter(
        SearchHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Search history not found"
        )

    for key, value in updated_history.dict().items():
        setattr(history, key, value)

    db.commit()
    db.refresh(history)

    return history


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_search_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    history = db.query(SearchHistory).filter(
        SearchHistory.id == history_id
    ).first()

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Search history not found"
        )

    db.delete(history)
    db.commit()

    return None