
from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base
from datetime import datetime
from sqlalchemy.orm import Relationship


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    products = Relationship("Product", back_populates="category")
