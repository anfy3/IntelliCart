from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Upsell
from app.schemas import UpsellCreate

router = APIRouter(prefix="/upsell", tags=["Upsell"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_upsell(
    upsell: UpsellCreate,
    db: Session = Depends(get_db)
):
    upsell_data = upsell.dict()
    upsell_data.pop("product_name", None)

    new_upsell = Upsell(**upsell_data)

    db.add(new_upsell)
    db.commit()
    db.refresh(new_upsell)

    return new_upsell


@router.get("/")
def get_upsells(db: Session = Depends(get_db)):
    return db.query(Upsell).all()


@router.get("/{upsell_id}")
def get_upsell(upsell_id: int, db: Session = Depends(get_db)):
    upsell = db.query(Upsell).filter(
        Upsell.id == upsell_id
    ).first()

    if not upsell:
        raise HTTPException(status_code=404, detail="Upsell not found")

    return upsell


@router.put("/{upsell_id}")
def update_upsell(
    upsell_id: int,
    updated_upsell: UpsellCreate,
    db: Session = Depends(get_db)
):
    upsell = db.query(Upsell).filter(
        Upsell.id == upsell_id
    ).first()

    if not upsell:
        raise HTTPException(status_code=404, detail="Upsell not found")

    upsell_data = updated_upsell.dict()
    upsell_data.pop("product_name", None)

    for key, value in upsell_data.items():
        setattr(upsell, key, value)

    db.commit()
    db.refresh(upsell)

    return upsell


@router.delete("/{upsell_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_upsell(
    upsell_id: int,
    db: Session = Depends(get_db)
):
    upsell = db.query(Upsell).filter(
        Upsell.id == upsell_id
    ).first()

    if not upsell:
        raise HTTPException(status_code=404, detail="Upsell not found")

    db.delete(upsell)
    db.commit()

    return None