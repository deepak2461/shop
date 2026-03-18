from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
import models.users
from models.orders import Order
import models.orders


from db.session import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

print("Models loaded successfully")