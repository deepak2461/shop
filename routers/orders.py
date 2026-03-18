

'''
POST /orders				🔐 Auth: Protected — Customer JWT required
GET /orders					🔐 Auth: Protected — JWT required. Admins see all orders; customers see only their own.
PATCH /orders/{id}/status   🔐 Auth: Protected — Admin JWT required

'''

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from services.order import *
from auth.security import get_current_user , require_role , require_admin

router = APIRouter(prefix="/orders" , tags=["orders"])


@router.get("/", response_model=OrderListResponse)
def list_orders(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "admin":
        if status or customer_id:
            raise HTTPException(403, "Query parameters allowed for admin role only")
    data =  get_orders(db, current_user, status, customer_id, page, limit)
    #return { **data.model_dump() , "message":f"SUCCESS -- {data.total} orders fetched Successfully"}
    #return {"order": data, "message":f"SUCCESS -- {data.total} orders fetched Successfully"}    # use response_model=OrderListResponseV 
    return data      # use response_model=OrderListResponse

#from schemas.gen import BaseResponseSchema


@router.post("/", response_model=OrderResponseV)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user), 
    #current_user: dict = Depends(require_role("customer")),
):
    if current_user["role"] != "customer":
        raise HTTPException(403, "Only customers can place orders")
    
    user_obj = db.query(Users).filter(Users.email == current_user["email"]).first()
    if not user_obj:
        raise HTTPException(401, "User not found")
    
    new_order = order_create(db, user_obj, order_data)
    return {"data": new_order, "message": f"SUCCESS -- Order with id - {new_order.id} created Successfully"}


@router.patch("/{id}/status", response_model=OrderResponseV)
def patch_order_status(id: str,data: OrderStatusUpdate,db: Session = Depends(get_db), current_user = Depends(require_admin)):
    updated_order =  update_order_status(db, id, data.status)
    return {"data": updated_order, "message": f"SUCCESS -- Order status updated Successfully to - {updated_order.status}"}