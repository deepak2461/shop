

from db.session import   get_db
from fastapi import Depends , HTTPException
from sqlalchemy.orm import Session , joinedload
from sqlalchemy import or_
from datetime import datetime
from math import ceil

from models.orders import *
from models.product import Product
from models.users import Users
from schemas.orders import *

def generate_order_id(db: Session) -> str:
    last = db.query(Order).order_by(Order.created_at.desc()).first()
    if not last:
        seq = 1
    else:
        seq = int(last.id.split('-')[1]) + 1
    return f"ORD-{seq:04d}"

def order_create(db: Session, user: Users, order: OrderCreate) :
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    total = 0
    item_count = 0
    order_items = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        #total += product.price * item.quantity
        subtotal = product.price * item.quantity
        total += subtotal
        item_count += item.quantity   # check this
        order_items.append(item)

    order.id = generate_order_id(db)
    order.user_id  = user.id
    order.customer_name  = user.name
    order.customer_email = user.email
    order.total = total
    order.item_count = item_count
    order.order_items = order_items
    db.add(order)
    db.commit()
    db.refresh(order)
    return order



def get_order_by_id(db: Session, order_id: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_orders(
        db: Session, 
        current_user : dict,
        status : str | None = None,
        customer_id : int | None = None,
        page: int = 1,
        limit: int = 10
        ):
    query = db.query(Order)

    if current_user["role"] != "admin":
        query = query.filter(Order.user_id == current_user["id"])

    else:
        if status:
            query = query.filter(Order.status == status)
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)

    total = query.count()
    orders = query.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    #return {"total": total, "orders": orders}
    return OrderListResponse(
            orders=[
                OrderResponse(
                            id=o.id,
                            customer=o.customer_name,
                            email=o.customer_email, 
                            items=[
                                    OrderItemResponse
                                    (
                                        product_id=item.product_id,
                                        product_name=item.product.name,
                                        quantity=item.quantity,
                                        subtotal=item.product.price * item.quantity
                                    )
                                    for item in o.order_items
                                ],
                                        item_count = o.item_count,
                                        total=o.total,
                                        status = o.status.value,
                                        date = o.created_at,
                            )
                            for o in orders
                        ],
                        total=total,
                        page=page,
                        pages=ceil(total / limit) if limit else 1,
                    )



def update_order_status(db: Session, order_id: str, new_status: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")

    try:
        order.status = enums.OrderStatus(new_status)
    except ValueError:
        raise HTTPException(400, "Invalid status value")

    db.commit()
    db.refresh(order)
    return order