from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from app.models import ClothingItem

router = APIRouter()

class ClothingItemRequest(BaseModel):
    name: str
    price: float
    quantity: int

class ClothingItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

@router.get("/clothing-items", response_model=List[ClothingItemResponse])
async def get_clothing_items():
    clothing_items = await ClothingItem.all()
    return clothing_items

@router.post("/clothing-items", response_model=ClothingItemResponse)
async def create_clothing_item(request: ClothingItemRequest):
    clothing_item = await ClothingItem.create(**request.dict())
    return clothing_item

@router.get("/clothing-items/{item_id}", response_model=ClothingItemResponse)
async def get_clothing_item(item_id: int):
    clothing_item = await ClothingItem.get(id=item_id)
    if not clothing_item:
        raise HTTPException(status_code=404, detail="Clothing item not found")
    return clothing_item

@router.put("/clothing-items/{item_id}", response_model=ClothingItemResponse)
async def update_clothing_item(item_id: int, request: ClothingItemRequest):
    clothing_item = await ClothingItem.get(id=item_id)
    if not clothing_item:
        raise HTTPException(status_code=404, detail="Clothing item not found")
    await clothing_item.update(**request.dict())
    return clothing_item

@router.delete("/clothing-items/{item_id}")
async def delete_clothing_item(item_id: int):
    clothing_item = await ClothingItem.get(id=item_id)
    if not clothing_item:
        raise HTTPException(status_code=404, detail="Clothing item not found")
    await clothing_item.delete()
    return JSONResponse(content={"message": "Clothing item deleted successfully"}, status_code=200)