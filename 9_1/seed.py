import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Product

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()

products = [
    Product(title="Ноутбук", price=75000, count=10),
    Product(title="Мышь", price=1200, count=50),
]
session.add_all(products)
session.commit()
print("Добавлено")