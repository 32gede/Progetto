from models import Product, Brand, Category
from sqlalchemy.orm import Session


def search_products(db_session, name, description, min_price, max_price, brand_name, category_name):
    query = db_session.query(Product)

    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if brand_name:
        query = query.join(Brand).filter(Brand.name.ilike(f"%{brand_name}%"))
    if category_name:
        query = query.join(Category).filter(Category.name.ilike(f"%{category_name}%"))

    return query.all()