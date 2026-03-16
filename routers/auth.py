# Routers related to the authentication page

# Endpoints   --  login, register                       


from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from auth.security import get_current_user
from schemas.user import *
from models.users import *
import services.auth
from auth.security import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth")

@router.post("/login" , response_model = UserSigninRes)
def login(request_model : UserSigninReq ,role : str, email:str, password:str, db : Session = Depends(get_db)):
    if not services.auth.user_exists(email, db):
        raise HTTPException(status_code=400, detail="User does not exist")
    else:
        user = services.auth.user_exists(email, db)
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid Credentials")
        else:
            access_token = create_access_token(request_model.model_dump())

            return {"data": request_model.model_dump(exclude={"password"}), "message": f"User logged in successfully","token": access_token}



    
@router.post("/register" , response_model = UserRegisterRes)
def register(request_model : UserRegisterReq , db : Session = Depends(get_db)):
    user = Users(**request_model.model_dump())
    if services.auth.user_exists(user.email, db): 
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        user.password = hash_password(user.password)
        #user.username = f"{user.name}_{user.id}"
        db.add(user)
        db.commit()
        db.refresh(user)

        user.username = f"{user.name}_{user.id}"
        db.commit()
        db.refresh(user)

        token = create_access_token(request_model.model_dump())
    
    
    return {"data": request_model.model_dump(exclude={"password"}), "message": f"User Registered successfully ---- Username: {user.username} and UserId: {user.id}", "token": token }
    