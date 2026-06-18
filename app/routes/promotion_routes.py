from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Promotion
from app.schemas import PromotionCreate

router = APIRouter(prefix="/promotions", tags=["Promotions"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_promotion(promotion: PromotionCreate, db: Session = Depends(get_db)):
    promotion_data = promotion.dict()
    promotion_data.pop("product_name", None)

    new_promotion = Promotion(**promotion_data)

    db.add(new_promotion)
    db.commit()
    db.refresh(new_promotion)

    return new_promotion


@router.get("/")
def get_promotions(db: Session = Depends(get_db)):
    return db.query(Promotion).all()


@router.get("/{promotion_id}")
def get_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()

    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    return promotion


@router.put("/{promotion_id}")
def update_promotion(
    promotion_id: int,
    updated_promotion: PromotionCreate,
    db: Session = Depends(get_db)
):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()

    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    promotion_data = updated_promotion.dict()
    promotion_data.pop("product_name", None)

    for key, value in promotion_data.items():
        setattr(promotion, key, value)

    db.commit()
    db.refresh(promotion)

    return promotion


@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()

    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    db.delete(promotion)
    db.commit()

    return None