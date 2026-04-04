from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models
from routers import users, products, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-Commerce API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
