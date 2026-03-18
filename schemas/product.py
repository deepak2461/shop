
# pydantic schemas for product

from pydantic import BaseModel, Field, field_validator , ConfigDict
from datetime import datetime
from typing import Optional


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class ProductResponse(BaseModel):
    id : int
    name : str
    category_id : int
    price : float
    stock : int
    sold : int
    emoji : str
    rating : Optional[float] = 0
    reviews : Optional[int] = 0
    description : str
    created_at : Optional[datetime] = None
    category : CategoryResponse             #Try to get categoy name  instead of category_id

    model_config = {
        "from_attributes": True
    }

class ProductListResponse(BaseModel):
    products : list[ProductResponse]
    total : int
    page : int
    limit : int

    model_config = {
        "from_attributes": True
    }


class ProductsResponse(BaseModel):
    products : list[ProductResponse]
    message : str

    model_config = {
        "from_attributes": True
    }




class CategoriesResponse(BaseModel):
    categories : list[CategoryResponse]
    message : str

    model_config = {
        "from_attributes": True
    }


class ProductRequest(BaseModel):
    name : str
    category : str
    price : float
    stock : int
    emoji : Optional[str] = None
    description : str

class ProductGenerators(ProductRequest):
    id : int
    sold : int = Field(default=0)
    rating : float = Field(default=0)
    reviews : int = Field(default=0)
    created_at : datetime = Field(default_factory=datetime.now)

class CreateProductResponse(BaseModel):
    products : ProductResponse
    message : str

    model_config = { "from_attributes": True }

class UpdateProductRequest(BaseModel):
    name : Optional[str] = None
    category : Optional[str] = None
    price : Optional[float] = None
    stock : Optional[int] = None
    emoji : Optional[str] = None
    description : Optional[str] = None

    model_config = ConfigDict(extra="forbid")   # prevents unknown fields


class UpdateProductRequestNotUsed(BaseModel):
    name: Optional[str] = Field(None,  json_schema_extra={"example": None})
    category: Optional[str] = Field(None,   json_schema_extra={"example": None})
    price: Optional[float] = Field(None,   json_schema_extra={"example": None})
    stock: Optional[int] = Field(None,   json_schema_extra={"example": None})
    emoji: Optional[str] = Field(None,   json_schema_extra={"example": None})
    description: Optional[str] = Field(None,   json_schema_extra={"example": None})

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {}}
    )

class DeleteProductResponse(BaseModel):
    message : str