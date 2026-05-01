import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Define the base directory and find the first HTML file
base_dir = Path(__file__).resolve().parent
html_files = list(base_dir.rglob('*.html'))

# Define a route for the root URL
@app.get('/')
def read_root():
    if not html_files:
        raise HTTPException(status_code=404, detail="No HTML file found")
    with open(html_files[0], 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

# Define a data model for clothing items
class ClothingItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str

# Define mock data for clothing items
clothing_items = [
    ClothingItem(id=1, name="Linen Blazer", description="Elegant linen blazer for summer", price=129.99, image_url="https://example.com/blazer.jpg"),
    ClothingItem(id=2, name="Cotton Dress", description="Comfortable cotton dress for casual wear", price=49.99, image_url="https://example.com/dress.jpg"),
    ClothingItem(id=3, name="Leather Jacket", description="Stylish leather jacket for winter", price=249.99, image_url="https://example.com/jacket.jpg"),
]

# Define a route for getting all clothing items
@app.get('/api/clothing')
def get_clothing():
    return clothing_items

# Define a route for getting a single clothing item by ID
@app.get('/api/clothing/{item_id}')
def get_clothing_item(item_id: int):
    for item in clothing_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Clothing item not found")

# Define a route for searching clothing items by name or description
@app.get('/api/clothing/search')
def search_clothing(q: str):
    results = [item for item in clothing_items if q.lower() in item.name.lower() or q.lower() in item.description.lower()]
    return results

# Define a route for getting the cart
@app.get('/api/cart')
def get_cart():
    # For now, return an empty cart
    return []

# Define a route for adding an item to the cart
@app.post('/api/cart')
def add_to_cart(item_id: int):
    # For now, just return a success message
    return {"message": "Item added to cart"}

# Define a route for removing an item from the cart
@app.delete('/api/cart/{item_id}')
def remove_from_cart(item_id: int):
    # For now, just return a success message
    return {"message": "Item removed from cart"}