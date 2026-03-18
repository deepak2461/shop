

from sqlalchemy import Column, Integer, String , DateTime, Float
from db.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



'''
products
---------
id	int	—	Unique product identifier
name	string	—	Product name
category_id	int	—	Category id
price	float	—	Price in USD (2 decimal places)
stock	int	—	Available stock count
sold	int	—	Total units sold
emoji	string	—	Single emoji used as product thumbnail
rating	float	—	Average rating 0–5
reviews	int	—	Total review count
description	string	—	Long-form product description
created_at	string	—	ISO 8601 timestamp


'''


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key = True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    sold = Column(Integer, nullable=False, default=0)
    emoji = Column(String, nullable=True)
    rating = Column(Float, nullable=True, default = 0 )
    reviews = Column(Integer, nullable=True, default = 0 )
    description = Column(String, nullable=False, default = "No description")
    created_at = Column(DateTime, nullable=True,default=datetime.now)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    reviews_list = relationship("Review", back_populates="product")