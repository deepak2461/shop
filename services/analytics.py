

from db.session import   get_db
from fastapi import Depends , HTTPException
from sqlalchemy.orm import Session , joinedload
from sqlalchemy import func , distinct
from datetime import datetime , timedelta
from math import ceil


from models.orders import Order , OrderItem
from models.product import Product
from models.category import Category
from schemas.analytics import *

def get_sales(sales_data: SalesRequest , db: Session):
    stats = db.query(
        func.sum(Order.total).label("total_sales"),
        func.count(Order.id).label("total_orders"),
        #func.count(distinct(Order.user_id)).label("total_customers_who_ordered")
    ).filter(Order.created_at.between(sales_data.start_date , sales_data.end_date)).first()

    total_sales = stats.total_sales or 0
    total_orders = stats.total_orders or 0
    #total_customers_who_ordered = stats.total_customers_who_ordered or 0
    avg_order = (total_sales / total_orders) if total_orders > 0 else 0

    data = SalesResponse(total_sales=total_sales , total_orders=total_orders , avg_order=avg_order)

    #return SalesResponse(total_sales=total_sales , total_orders=total_orders , avg_order=total_sales/total_orders)
    return {"data":data , "message":"SUCCESS -- Sales Stats Fetched Successfully"}

def get_monthly(monthly_data: MonthlyRequest , db: Session):
    start_date = datetime.now() - timedelta(days=30 * monthly_data.months)
    orders = db.query(Order).filter(Order.created_at.between(start_date , datetime.now())).all()

    monthly_dict = {}

    for order in orders:
        month_key = order.created_at.strftime("%Y-%m")          # getting multimonths, chage this
        if month_key not in monthly_dict:
            monthly_dict[month_key] = {
                "total_sales": 0,
                "total_orders": 0,
                "year": order.created_at.year,
                "month": order.created_at.strftime("%B")
                
            }    

        monthly_dict[month_key]["total_sales"] += order.total
        monthly_dict[month_key]["total_orders"] += 1

    #return {"data": list(monthly_data.values()) , "message":"SUCCESS -- Monthly Stats Fetched Successfully"}
    #return list(monthly_data.values())
    #return monthly_data
    final_res = []
    for stat in monthly_dict.values():
        stat["avg_order"] = (stat["total_sales"] / stat["total_orders"]) if stat["total_orders"] > 0 else 0
        final_res.append(stat)

    return {"data" : final_res}

    

def get_categories(db: Session):
    total_sales = db.query(func.sum(Order.total)).first()[0] or 0

    if total_sales == 0:
        raise HTTPException(400, "No Sales Fount")
    
    results = db.query(
        Category.name,
        # func.sum(Order.total).label("total_sales"),
        # func.count(Order.id).label("total_orders")
        func.sum(OrderItem.subtotal).label("total_sales"),
        func.count(OrderItem.id).label("total_orders")

    ).select_from(OrderItem).join(Product, OrderItem.product_id == Product.id)\
                            .join(Category, Product.category_id == Category.id)\
                            .group_by(Category.name).all()
    
    category_data = []
    for result in results:
        sales = result.total_sales or 0
        orders = result.total_orders or 0
        pct = (sales / total_sales) * 100

        category_data.append(CategoryStat(
            category=result.name,
            total_sales=sales,
            pct=round(pct, 2),  # 99.90791161950317
            total_orders=orders

        ))
    return {"data": {"data": category_data} , "message":"SUCCESS -- Category Stats Fetched Successfully"}
