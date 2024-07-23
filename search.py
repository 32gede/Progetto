from models import Product, Brand, Category
from sqlalchemy.orm import Session

def search_products(session: Session, name: str = None, description: str = None, min_price: int = None, max_price: int = None, brand_name: str = None, category_name: str = None):
    query = session.query(Product)

    if name:
        query = query.filter(Product.name.like(f'%{name}%'))
    if description:
        query = query.filter(Product.description.like(f'%{description}%'))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if brand_name:
        query = query.join(Product.brand).filter(Brand.name.like(f'%{brand_name}%'))
    if category_name:
        query = query.join(Product.category).filter(Category.name.like(f'%{category_name}%'))

    return query.all()