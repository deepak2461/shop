

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from auth.security import get_current_user, require_role , require_admin
from schemas.user import CustomerResponseV
from services.customer import get_customers


router = APIRouter(prefix="/customers" , tags=["Customers"])

@router.get("/", response_model=CustomerResponseV)
def list_customers(db: Session = Depends(get_db), current_user: dict = Depends(require_admin)):
    customers =  get_customers(db)
    return {"data": customers, "message": f"SUCCESS -- {len(customers)} customers fetched Successfully"}
