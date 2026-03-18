
import models.users
from db.session import   get_db
from fastapi import Depends , HTTPException
from sqlalchemy.orm import Session , joinedload
from sqlalchemy import or_

from models.product import Product
from models.category import Category



def get_products(db: Session, search, category, page, limit, sort):
    
    query = db.query(Product)
    #query = db.query(Product).join(Category)

    if category:
        query = query.join(Category).filter(Category.name == category)
        #query = query.filter(Category.name == category)
        #query = query.filter(Product.category.name == category)     # AttributeError: Neither 'InstrumentedAttribute' object nor 'Comparator' object associated with Product.category has an attribute 'name'


 
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
            )
        )

    if sort == "price_asc":
        query = query.order_by(Product.price.asc())

    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())

    elif sort == "rating":
        query = query.order_by(Product.rating.desc())

    elif sort == "latest":
        query = query.order_by(Product.created_at.desc())

    total = query.count()
    print(total)

    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()
    # print("#" * 22)
    # print(products)
    # print("#" * 22)

    return {
        "products": products,
        "total": total,
        "page": page,
        "limit": limit,
    }


def show_product_by_id(db: Session, id:int):
    #print(db.query(Product).filter(Product.id == id).first())
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == id).first()


def show_product_by_category(db: Session, category: str):
    if db.query(Category).filter(Category.name == category).count():
        return db.query(Product).join(Category).filter(Category.name == category).all()
    else : 
        raise HTTPException(status_code=404, detail="Category not found")
    #return db.query(Product).join(Category).filter(Category.name == category).all()



def list_categories(db: Session):
    return db.query(Category).all()


def product_create(db: Session, product: Product):

    if db.query(Product).filter(Product.name == product.name).count():
        raise HTTPException(status_code=400, detail="Product already exists")

    category = db.query(Category).filter(Category.name == product.category).first()

    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    

    new_product = Product(
        name = product.name,
        category_id = category.id,
        price = product.price,
        stock = product.stock,
        emoji = product.emoji,
        description = product.description,
    )
    new_product.id = None               # Added for letting db decide the id (reg. manual additions in db)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def product_update(db: Session, product: Product , id : int):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_fields = product.model_dump(exclude_unset=True, exclude_none=True)  # remove unset fields and converts only provided fields into dict

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    
    if "category" in update_fields:
        category_name = update_fields.pop("category")  
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            raise HTTPException(status_code=400, detail=f"Category '{category_name}' not found")
        db_product.category_id = category.id
 
    for field, value in update_fields.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product

'''
    category = db.query(Category).filter(Category.name == product.category).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    else:
        db_product.name = product.name
        db_product.category_id = category.id
        db_product.price = product.price
        db_product.stock = product.stock
        db_product.emoji = product.emoji
        db_product.description = product.description
        db.commit()
        db.refresh(db_product)
        return db_product
'''


def product_delete(db: Session, id: int):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}