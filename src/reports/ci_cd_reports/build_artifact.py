
# --- main.py ---
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

# --- index.html ---
<html>
<head>
    <title>Clothe Shopping Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        .header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        .nav-bar {
            background-color: #444;
            padding: 10px;
            text-align: center;
        }
        .nav-bar a {
            color: #fff;
            text-decoration: none;
            margin: 10px;
        }
        .main-content {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        .product-card {
            background-color: #fff;
            margin: 20px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        .product-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px 10px 0 0;
        }
        .product-card h2 {
            font-size: 18px;
            margin-top: 10px;
        }
        .product-card p {
            font-size: 14px;
            color: #666;
        }
        .product-card button {
            background-color: #333;
            color: #fff;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .product-card button:hover {
            background-color: #444;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Clothe Shopping Dashboard</h1>
    </div>
    <div class="nav-bar">
        <a href="#">Men</a>
        <a href="#">Women</a>
        <a href="#">Kids</a>
    </div>
    <div class="main-content">
        <div class="product-card">
            <img src="https://via.placeholder.com/300x200?text=Men+Shirt" alt="Men Shirt">
            <h2>Men's Cotton Shirt</h2>
            <p>High quality cotton shirt for men. Available in various colors and sizes.</p>
            <p>Price: $25.99</p>
            <button>Add to Cart</button>
        </div>
        <div class="product-card">
            <img src="https://via.placeholder.com/300x200?text=Women+Dress" alt="Women Dress">
            <h2>Women's Summer Dress</h2>
            <p>Beautiful summer dress for women. Made from high quality fabric.</p>
            <p>Price: $39.99</p>
            <button>Add to Cart</button>
        </div>
        <div class="product-card">
            <img src="https://via.placeholder.com/300x200?text=Kids+T-Shirt" alt="Kids T-Shirt">
            <h2>Kids' T-Shirt</h2>
            <p>Cute and comfortable t-shirt for kids. Available in various colors and sizes.</p>
            <p>Price: $14.99</p>
            <button>Add to Cart</button>
        </div>
    </div>
    <script>
        // Add event listener to button clicks
        const buttons = document.querySelectorAll('.product-card button');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                // Add product to cart logic here
                alert('Product added to cart!');
            });
        });
    </script>
</body>
</html>

# --- requirements.txt ---
fastapi
uvicorn
