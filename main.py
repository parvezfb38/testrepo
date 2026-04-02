from fastapi import FastAPI
from database import engine
import models
from routers import users, products, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-Commerce API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Mini E-Commerce API"}
