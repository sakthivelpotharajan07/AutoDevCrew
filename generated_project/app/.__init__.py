from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    product,
    order,
    user
)

app = FastAPI(title="Clothe Shopping Dashboard")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    product.router,
    prefix="/product",
    tags=["Product"]
)
app.include_router(
    order.router,
    prefix="/order",
    tags=["Order"]
)
app.include_router(
    user.router,
    prefix="/user",
    tags=["User"]
)