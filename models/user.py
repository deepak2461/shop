
#Pydantic models for user request and response bodies
# Req -- Request body
# Res -- Response body

from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class UserSigninReq(BaseModel):
    role : str
    email: str
    password: str

class UserRegisterReq(BaseModel):
    name : str
    email : str
    password : str
    role : str = Field(default="customer")

    @field_validator("password")
    def validate_password(cls, value):
        if len(value)<3:
            raise ValueError("pwd must be more than 3 chars")
        return value


class UserSigninRes(UserSigninReq):
    token : str
    id : int

class UserRegisterRes(UserRegisterReq):
    id : int
    username : str
    created_at : datetime = Field(default_factory = datetime.now())

    model_config = {                # It tells Pydantic: If input is an object, read its attributes instead of expecting dict.
        "from_attributes": True     # This configuration allows Pydantic to create a User model instance from an instance of the db_models.User class, which is useful when retrieving user data from the database and returning it in the API response.
    }



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