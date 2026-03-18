# SQL Alchemy models for user related database tables


from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

import enums
from db.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role : enums.UserRole = Column(String, nullable=False, default="customer")
    created_at = Column(DateTime, default=datetime.now())

    orders = relationship("Order", back_populates="user")