from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CrossSell
from app.schemas import CrossSellCreate

router = APIRouter(prefix="/cross-sell", tags=["Cross Sell"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_cross_sell(
    cross_sell: CrossSellCreate,
    db: Session = Depends(get_db)
):
    cross_sell_data = cross_sell.dict()
    cross_sell_data.pop("product_name", None)

    new_cross_sell = CrossSell(**cross_sell_data)

    db.add(new_cross_sell)
    db.commit()
    db.refresh(new_cross_sell)

    return new_cross_sell


@router.get("/")
def get_cross_sells(db: Session = Depends(get_db)):
    return db.query(CrossSell).all()


@router.get("/{cross_sell_id}")
def get_cross_sell(cross_sell_id: int, db: Session = Depends(get_db)):
    cross_sell = db.query(CrossSell).filter(
        CrossSell.id == cross_sell_id
    ).first()

    if not cross_sell:
        raise HTTPException(status_code=404, detail="Cross sell not found")

    return cross_sell


@router.put("/{cross_sell_id}")
def update_cross_sell(
    cross_sell_id: int,
    updated_cross_sell: CrossSellCreate,
    db: Session = Depends(get_db)
):
    cross_sell = db.query(CrossSell).filter(
        CrossSell.id == cross_sell_id
    ).first()

    if not cross_sell:
        raise HTTPException(status_code=404, detail="Cross sell not found")

    cross_sell_data = updated_cross_sell.dict()
    cross_sell_data.pop("product_name", None)

    for key, value in cross_sell_data.items():
        setattr(cross_sell, key, value)

    db.commit()
    db.refresh(cross_sell)

    return cross_sell


@router.delete("/{cross_sell_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cross_sell(
    cross_sell_id: int,
    db: Session = Depends(get_db)
):
    cross_sell = db.query(CrossSell).filter(
        CrossSell.id == cross_sell_id
    ).first()

    if not cross_sell:
        raise HTTPException(status_code=404, detail="Cross sell not found")

    db.delete(cross_sell)
    db.commit()

    return None