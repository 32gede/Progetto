from hashlib import md5

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, event, Float, LargeBinary, Text
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta

Base = declarative_base()


# -------------- Utenti:

class User(UserMixin, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[bytes] = mapped_column(String(255), nullable=True)
    insert_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # New fields
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)

    seller: Mapped["UserSeller"] = relationship("UserSeller", uselist=False, back_populates="user", lazy='joined') # Eager loading
    buyer: Mapped["UserBuyer"] = relationship("UserBuyer", uselist=False, back_populates="user")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
    cart_items: Mapped["CartItem"] = relationship("CartItem", back_populates="user")
    orders: Mapped["Order"] = relationship("Order", back_populates="user")
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'), nullable=True)
    address: Mapped["Address"] = relationship("Address", back_populates="users")

    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        # Restituisce l'ID dell'utente come stringa
        return str(self.id)

    def gravatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relazioni con users e orders
    users: Mapped[list["User"]] = relationship("User", back_populates="address")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="address")

    def __repr__(self):
        return f"Address({self.address}, {self.city})"

    def __str__(self):
        return f"{self.address}, {self.city}"


class UserSeller(Base):
    __tablename__ = 'user_sellers'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    seller_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="seller")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="seller")


# -------------- Prodotti:

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[bytes] = mapped_column(String(255), nullable=True)
    insert_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey('brands.id'), nullable=True)
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_sellers.id'), nullable=True)
    seller: Mapped["UserSeller"] = relationship("UserSeller", back_populates="products")

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="product")
    cart_items: Mapped["CartItem"] = relationship("CartItem", back_populates="product")
    order_items: Mapped["OrderItem"] = relationship("OrderItem", back_populates="product")


class Brand(Base):
    __tablename__ = 'brands'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped["Product"] = relationship("Product", back_populates="brand")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped["Product"] = relationship("Product", back_populates="category")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped["User"] = relationship("User", back_populates="reviews")
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # Timestamp aggiunto

    user: Mapped["User"] = relationship("User", back_populates="cart_items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # Data di conferma
    total: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='In attesa')  # Stati dell'ordine

    user: Mapped["User"] = relationship("User", back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'), nullable=True)
    address: Mapped["Address"] = relationship("Address", back_populates="orders")

    def update_status_based_on_time(self):
        if self.status == 'Confermato' and self.confirmed_at:
            # Aggiorna lo stato a "Spedito" dopo 2 giorni
            if datetime.utcnow() >= self.confirmed_at + timedelta(days=2):
                self.status = 'Spedito, consegna prevista entro 3 giorni'
            # Aggiorna lo stato a "Consegnato" dopo 5 giorni
            if datetime.utcnow() >= self.confirmed_at + timedelta(days=5):
                self.status = "Consegnato"


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)  # Prezzo aggiunto

    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")
