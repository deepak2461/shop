
import models.users
from db.session import   get_db
from fastapi import Depends
from sqlalchemy.orm import Session



def user_exists(email, db: Session = Depends(get_db)):
    return db.query(models.users.Users).filter(models.users.Users.email == email).first()