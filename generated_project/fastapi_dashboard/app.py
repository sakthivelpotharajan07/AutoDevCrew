from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from typing import List
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Product(BaseModel):
    id: int
    name: str
    description: str
    image_url: str
    price: float
    sizes: List[str]

class Order(BaseModel):
    id: int
    customer_name: str
    order_date: datetime
    total_amount: float

class ProductItem(BaseModel):
    product: Product
    quantity: int

class User(BaseModel):
    id: int
    name: str
    email: str

# Mock data
products = [
    Product(id=1, name="Denim Jacket", description="A classic denim jacket.", image_url="jacket.jpg", price=50.0, sizes=["M", "L"]),
    Product(id=2, name="Sneakers", description="Comfy and stylish sneakers.", image_url="sneakers.jpg", price=80.0, sizes=["8", "10"]),
    Product(id=3, name="Hoodie", description="Soft and cozy hoodie.", image_url="hoodie.jpg", price=40.0, sizes=["S", "M"]),
]

users = [
    User(id=1, name="John Doe", email="john.doe@example.com"),
    User(id=2, name="Jane Doe", email="jane.doe@example.com"),
]

orders = [
    Order(id=1, customer_name="John Doe", order_date=datetime(2023, 1, 1), total_amount=100.0),
    Order(id=2, customer_name="Jane Doe", order_date=datetime(2023, 1, 15), total_amount=150.0),
]

product_items = [
    ProductItem(product=products[0], quantity=2),
    ProductItem(product=products[1], quantity=1),
    ProductItem(product=products[2], quantity=3),
]

# Route for the home page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("home.html", {"request": "GET request"})

# Route for the products page
@app.get("/products/")
async def read_products():
    return {"products": [{"name": p.name, "price": f"${p.price}"} for p in products]}

# Route for the product item page
@app.get("/product/{product_id}")
async def read_product(product_id: str):
    product = next((p for p in products if p.id == int(product_id)), None)
    if product:
        return {"product": {"name": product.name, "price": f"${product.price}"}}
    return {"error": "Product not found"}

# Route for the orders page
@app.get("/orders/")
async def read_orders():
    return {"orders": [{"id": o.id, "customer_name": o.customer_name} for o in orders]}

# Route for uploading a new product image
@app.post("/upload-image/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Route for logging in a user
@app.post("/login/")
async def login_user(user: User):
    return {"message": f"Welcome {user.name}!"}

# Route for making a new order
@app.post("/order/")
async def make_order(order: Order):
    return {"message": f"Order {order.id} made successfully!"}

# Route for a user's order history
@app.get("/user/{user_id}/orders/")
async def read_user_orders(user_id: str):
    user = next((u for u in users if u.id == int(user_id)), None)
    if user:
        return {"orders": [{"id": o.id, "customer_name": o.customer_name} for o in orders if o.customer_name == user.name]}
    return {"error": "User not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)