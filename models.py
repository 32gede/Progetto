from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    seller: Mapped["UserSeller"] = relationship("UserSeller", uselist=False, back_populates="user")
    buyer: Mapped["UserBuyer"] = relationship("UserBuyer", uselist=False, back_populates="user")

class UserSeller(Base):
    __tablename__ = 'user_sellers'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    seller_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="seller")
    products: Mapped["Product"] = relationship("Product", back_populates="user_sellers")

class UserBuyer(Base):
    __tablename__ = 'user_buyers'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    buyer_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="buyer")

# --------------------------------------

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey('brands.id'), nullable=True)
    brand : Mapped["Brand"] = relationship("Brand", back_populates="products")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=True)
    category: Mapped["category"] = relationship("Category", back_populates="products")
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_sellers.id'), nullable=True)
    seller: Mapped["user_sellers"] = relationship("UserSeller", back_populates="user_sellers")

class Brand(Base):
    __tablename__ = 'brands'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped["Product"] = relationship("Product", back_populates="brand")

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped["Product"] = relationship("Product", back_populates="category")