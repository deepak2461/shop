# Pydantic models / Schemas for user request and response bodies
# Req -- Request body
# Res -- Response body

from pydantic import BaseModel, Field, field_validator
from datetime import datetime

import enums
import schemas.gen
#from auth.security import create_access_token, hash_password

class UserSigninReq(BaseModel):
    role : enums.UserRole
    email: str
    password: str

class UserRegisterReq(BaseModel):
    name : str
    email : str
    password : str
    role : enums.UserRole = Field(default=enums.UserRole.customer)

    @field_validator("password")
    def validate_password(cls, value):
        if len(value)<3:
            raise ValueError("pwd must be more than 3 chars")
        return value
    
    model_config = {
        "from_attributes": True
    }


# class UserSigninRes(schemas.gen.BaseResponseSchema):
#     token : str

class UserSigninRes(BaseModel):
    access_token : str
    token_type : str


class UserRegisterRes(schemas.gen.BaseResponseSchema):
    token : str
    created_at : datetime = Field(default_factory = datetime.now)

    model_config = {                # It tells Pydantic: If input is an object, read its attributes instead of expecting dict.
        "from_attributes": True     # This configuration allows Pydantic to create a User model instance from an instance of the db_models.User class, which is useful when retrieving user data from the database and returning it in the API response.
    }

'''
class UserSigninRes(UserSigninReq):
    token : str         #= Field(default_factory = lambda: create_access_token({"sub": "user_id"}))
    id : int

class UserRegisterRes(UserRegisterReq):
    token : str         #= Field(default_factory = lambda: create_access_token({"sub": "user_id"}))
    id : int
    username : str
    created_at : datetime = Field(default_factory = datetime.now)

    model_config = {                
        "from_attributes": True     
    }



'''


'''
class User(BaseModel):
    id: int
    email: str
    name : str
    username: str 
    password: str
    role : str = Field(default="customer")
    created_at: datetime = Field(default_factory = datetime.now())

    @field_validator("password")
    def validate_password(cls, value):
        if len(value)<3:
            raise ValueError("Pwd must be more than 3 chars")
        return value
    

class UserCreate(BaseModel):

'''

class CustomerResponse(BaseModel):
    id : int
    name  : str
    username : str
    email : str
    role : enums.UserRole
    created_at : datetime

    model_config = {
        "from_attributes": True
    }

class CustomerResponseV(BaseModel):
    data : list[CustomerResponse]
    message : str
    




