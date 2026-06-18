from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Recommendation
from app.schemas import RecommendationCreate

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):
    recommendation_data = recommendation.dict()

    # Schema has extra fields not present in DB model
    recommendation_data.pop("product_name", None)
    alternative_option = recommendation_data.pop("alternative_option", None)

    # Schema uses recommendation_reason, DB model uses reason
    reason = recommendation_data.pop("recommendation_reason")

    new_recommendation = Recommendation(
        reason=reason,
        **recommendation_data
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return {
        "id": new_recommendation.id,
        "product_id": new_recommendation.product_id,
        "recommendation_reason": new_recommendation.reason,
        "confidence_score": new_recommendation.confidence_score,
        "alternative_option": alternative_option
    }


@router.get("/")
def get_recommendations(db: Session = Depends(get_db)):
    return db.query(Recommendation).all()


@router.get("/{recommendation_id}")
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return recommendation


@router.put("/{recommendation_id}")
def update_recommendation(
    recommendation_id: int,
    updated_recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    recommendation_data = updated_recommendation.dict()
    recommendation_data.pop("product_name", None)
    recommendation_data.pop("alternative_option", None)

    reason = recommendation_data.pop("recommendation_reason")

    recommendation.reason = reason

    for key, value in recommendation_data.items():
        setattr(recommendation, key, value)

    db.commit()
    db.refresh(recommendation)

    return recommendation


@router.delete("/{recommendation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db)
):
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    db.delete(recommendation)
    db.commit()

    return None