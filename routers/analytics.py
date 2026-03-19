
'''

GET	/api/analytics/sales	Aggregate revenue, order, and customer totals
GET	/api/analytics/monthly	Per-month revenue and order counts for charting
GET	/api/analytics/categories	Revenue share by product category

'''

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from auth.security import require_admin 

from schemas.analytics import *
from services.analytics import *

router = APIRouter(prefix="/analytics" , tags=["Analytics"])


@router.get("/sales" , dependencies=[Depends(require_admin)], response_model=SalesResponseV)
def get_sales_stats(request_model : SalesRequest = Depends() , db: Session = Depends(get_db)):
    return get_sales(request_model, db)

@router.get("/monthly" , dependencies=[Depends(require_admin)], response_model=MonthlyResponse)
def get_monthly_stats(request_model : MonthlyRequest = Depends() , db: Session = Depends(get_db)):    #	TypeError: Failed to execute 'fetch' on 'Window': Request with GET/HEAD method cannot have body.
    return  get_monthly(request_model, db)

@router.get("/categories" , dependencies=[Depends(require_admin)], response_model=CategoryResponseV)
def get_categories_stats(db: Session = Depends(get_db)):
    return get_categories(db)

