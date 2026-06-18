from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Review
from app.schemas import ReviewCreate

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    review_data = review.dict()
    review_data.pop("product_name", None)

    new_review = Review(**review_data)

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.get("/")
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.get("/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


@router.put("/{review_id}")
def update_review(review_id: int, updated_review: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review_data = updated_review.dict()
    review_data.pop("product_name", None)

    for key, value in review_data.items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return None