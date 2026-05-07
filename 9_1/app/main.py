from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Task 9_1 - Alembic migrations"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()