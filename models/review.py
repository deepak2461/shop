

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from db.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False) 
    text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="reviews_list")
    user = relationship("Users", back_populates="reviews")