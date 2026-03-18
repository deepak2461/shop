

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from auth.security import get_current_user, require_role

from schemas.review import ReviewCreate, ReviewResponse
from services.review import add_review
from models.review import Review

router = APIRouter(prefix="/products", tags=["Reviews"])

@router.get("/{id}/reviews", response_model=List[ReviewResponse])
def get_product_reviews(id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == id).all()
    return [
        ReviewResponse(
            id=r.id,
            product_id=r.product_id,
            user=r.user.name,
            rating=r.rating,
            text=r.text,
            date=r.created_at
        ) for r in reviews
    ]

@router.post("/{id}/reviews", response_model=ReviewResponse, status_code=201)
def post_review(
    id: int, 
    review_data: ReviewCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("customer"))
):

    from models.users import Users
    user = db.query(Users).filter(Users.email == current_user["email"]).first()
    
    review = add_review(db, id, user.id, user.name, review_data)
    
    return ReviewResponse(
        id=review.id,
        product_id=review.product_id,
        user=user.name,
        rating=review.rating,
        text=review.text,
        date=review.created_at
    )