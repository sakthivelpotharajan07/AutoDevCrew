from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel, InputValidationError
from typing import List, Dict
from app import db, schemes
from app.auth import get_current_user

router = APIRouter(
    tags=["Clothes"],
    responses={500: {"description": "Internal Server Error"}},
)

class ClothesSchema(BaseModel):
    id: int
    name: str
    price: float
    brand: str

class ClothesRequest(BaseModel):
    name: str
    price: float
    brand: str

@router.get("/clothes", response_model=List[ClothesSchema])
async def get_clothes(db: Session = Depends(db.get_db)):
    return db.query(schemes.Clothe).all()

@router.get("/clothes/{clothe_id}", response_model=ClothesSchema)
async def get_cloth(cloth_id: int, db: Session = Depends(db.get_db)):
    cloth = db.query(schemes.Clothe).filter(schemes.Clothe.id == cloth_id).first()
    if not cloth:
        raise HTTPException(status_code=404, detail="Clothe not found")
    return cloth

@router.post("/clothes", response_model=ClothesSchema)
async def create_clothes(
    cloth: InputValidationError,
    db: Session = Depends(db.get_db),
    current_user: schemes.User = Depends(get_current_user)
):
    try:
        new_cloth = schemes.Clothe(name=cloth.name, price=cloth.price, brand=cloth.brand, owner_id=current_user.id)
        db.add(new_cloth)
        db.commit()
        db.flush()
        return new_cloth
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data")

@router.put("/clothes/{cloth_id}", response_model=ClothesSchema)
async def update_cloth(
    cloth_id: int,
    cloth_data: InputValidationError,
    db: Session = Depends(db.get_db),
    current_user: schemes.User = Depends(get_current_user)
):
    cloth = db.query(schemes.Clothe).filter(schemes.Clothe.id == cloth_id).first()
    if not cloth:
        raise HTTPException(status_code=404, detail="Clothe not found")
    if cloth.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden action")
    try:
        if cloth_data.name:
            cloth.name = cloth_data.name
        if cloth_data.price:
            cloth.price = cloth_data.price
        if cloth_data.brand:
            cloth.brand = cloth_data.brand
        db.add(cloth)
        db.commit()
        db.flush()
        return cloth
    except InputValidationError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data")