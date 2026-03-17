
# Products related router file

# GET /categories
# GET /products
# GET /products/{id}
# GET /products/{categories}
# POST /products			 Auth: Protected — Admin JWT required
# PUT /products/{id}		 Auth: Protected — Admin JWT required
# DELETE /products/{id}	     Auth: Protected — Admin JWT required	

from fastapi import APIRouter , Depends , HTTPException , Query
from sqlalchemy.orm import Session
from typing import List


from schemas.product import ProductResponse, ProductListResponse , ProductsResponse , CategoriesResponse  , ProductRequest
from db.session import get_db
from services.product import get_products , show_product_by_id , show_product_by_category , list_categories , product_create
from auth.security import require_admin

router = APIRouter(prefix="/products")


@router.get("/", response_model=ProductListResponse)
def list_products(search: str | None = None , 
                  category: str | None = None, 
                  page: int = Query(1, ge=1), 
                  limit: int = Query(20, ge=1, le=100), 
                  sort: str | None = None, 
                  db: Session = Depends(get_db)):
    return get_products(db, search, category, page, limit, sort)


@router.get("/category", response_model = CategoriesResponse)
def get_categories(db: Session = Depends(get_db)):
    cats = list_categories(db)
    if not cats:
        raise HTTPException(status_code=404, detail="No Categories found")
    else:
        return {"categories": cats , "message": f"Success -- Found {len(cats)} categories"}
    

@router.get("/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = show_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return product

@router.get("/category/{category}", response_model=ProductsResponse)
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    products = show_product_by_category(db, category)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found in given category")
    else:
        return {"products": products , "message": "Success"}
    


# Auth: Protected — Admin JWT required

@router.post("/", response_model=ProductsResponse)
def create_product(product: ProductRequest, db: Session = Depends(get_db) , current_user = Depends(require_admin)):
    product = product_create(db, product)
    return {"products": product , "message": f"Success -- Crated product with id - {product.id}"}