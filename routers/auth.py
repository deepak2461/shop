# Routers related to the authentication page

# Endpoints   --  login, register                       


from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from auth.security import get_current_user
from schemas.user import *
from models.users import *
from auth.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth")

@router.post("/login" , response_model = UserSigninRes)
def login(request_model : UserSigninReq ,role : str, email:str, password:str, db : Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


    
    
    

    
@router.post("/register" , response_model = UserRegisterRes)
def register(request_model : UserRegisterReq , db : Session = Depends(get_db)):
    pass
    