

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from models.review import Review
from models.product import Product
from schemas.review import ReviewCreate


def add_review(db: Session, product_id: int, user_id: int, user_name: str, review_in: ReviewCreate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    existing = db.query(Review).filter(Review.product_id == product_id, Review.user_id == user_id).first()
    if existing:
        raise HTTPException(409, "Product already reviewed by user")

    new_review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=review_in.rating,
        text=review_in.text
    )
    db.add(new_review)
    
    all_ratings = db.query(Review.rating).filter(Review.product_id == product_id).all()
    ratings_list = [r[0] for r in all_ratings] + [review_in.rating]
    
    product.reviews = len(ratings_list)
    product.rating = round(sum(ratings_list) / len(ratings_list), 2)

    db.commit()
    db.refresh(new_review)
    return new_review