
from sqlalchemy import Column, Integer, String , DateTime, Float
from db.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import enums



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String(10), ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    product = relationship("Product", back_populates="order_items")
    order = relationship("Order", back_populates="items")



class Order(Base):
    __tablename__ = "orders"

    id = Column(String(10), primary_key=True)           # ORD-0001 style
    user_id  = Column(Integer, ForeignKey("users.id"), nullable=True) 
    customer_name  = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    #items : list[OrderItem] = []                       
    status : enums.OrderStatus = Column(String, nullable=False, default="pending")
    total = Column(Float(precision=2), nullable=False)
    item_count  = Column(Integer, nullable=False)
    created_at  = Column(DateTime, server_default=func.now(), nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")     # Without delete-orphan, removing an item from order.items would just set its order_id to NULL → leaving orphaned rows (bad data).
    user = relationship("Users", back_populates="orders")


