
from models.users import Users
from sqlalchemy.orm import Session


def get_customers(db: Session):
    return db.query(Users).filter(Users.role == "customer").all()