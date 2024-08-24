from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin
from datetime import datetime, timedelta

Base = declarative_base()


# -------------- Utenti:

class User(UserMixin, Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        role (str): The role of the user.
        avatar (bytes): The avatar image of the user.
        insert_date (datetime): The date the user was added to the system.
        name (str): The full name of the user.
        username (str): The username of the user.
        seller (UserSeller): The seller profile associated with the user.
        reviews (list[Review]): The reviews written by the user.
        cart_items (list[CartItem]): The items in the user's cart.
        orders (list[Order]): The orders placed by the user.
        address_id (int): The ID of the user's address.
        address (Address): The address associated with the user.
    """
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

    seller: Mapped["UserSeller"] = relationship("UserSeller", uselist=False, back_populates="user", lazy='joined')
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
    cart_items: Mapped["CartItem"] = relationship("CartItem", back_populates="user")
    orders: Mapped["Order"] = relationship("Order", back_populates="user")
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('addresses.id'), nullable=True)
    address: Mapped["Address"] = relationship("Address", back_populates="users")

    @property
    def password_hash(self):
        """
        Get the hashed password of the user.

        Returns:
            str: The hashed password.
        """
        return self.password

    @password_hash.setter
    def password_hash(self, password):
        """
        Set the hashed password of the user.

        Args:
            password (str): The plain text password to hash and set.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The plain text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)

    def get_id(self):
        """
        Get the ID of the user as a string.

        Returns:
            str: The ID of the user.
        """
        return str(self.id)

    def gravatar(self, size):
        """
        Get the Gravatar URL for the user's email.

        Args:
            size (int): The size of the Gravatar image.

        Returns:
            str: The Gravatar URL.
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Address(Base):
    """
    Represents an address in the system.

    Attributes:
        id (int): The unique identifier for the address.
        address (str): The street address.
        city (str): The city of the address.
        users (list[User]): The users associated with the address.
        orders (list[Order]): The orders associated with the address.
    """
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relazioni con users e orders
    users: Mapped[list["User"]] = relationship("User", back_populates="address")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="address")

    def __repr__(self):
        """
        Get a string representation of the address. This is used for debugging.

        Returns:
            str: The string representation of the address.
        """
        return f"Address({self.address}, {self.city})"

    def __str__(self):
        """
        Get a string representation of the address. This is used for displaying the address.

        Returns:
            str: The string representation of the address.
        """
        return f"{self.address}, {self.city}"


class UserSeller(Base):
    """
    Represents a seller profile for a user.

    Attributes:
        id (int): The unique identifier for the seller (same as the user ID).
        seller_rating (int): The rating of the seller.
        user (User): The user associated with the seller profile.
        products (list[Product]): The products sold by the seller.
    """
    __tablename__ = 'user_sellers'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    seller_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="seller")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="seller")


# -------------- Prodotti:

class Product(Base):
    """
    Represents a product in the system.

    Attributes:
        id (int): The unique identifier for the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        quantity (int): The quantity of the product in stock.
        image (bytes): The image of the product.
        insert_date (datetime): The date the product was added to the system.
        brand_id (int): The ID of the brand associated with the product.
        brand (Brand): The brand associated with the product.
        category_id (int): The ID of the category associated with the product.
        category (Category): The category associated with the product.
        seller_id (int): The ID of the seller associated with the product.
        seller (UserSeller): The seller associated with the product.
        reviews (list[Review]): The reviews for the product.
        cart_items (list[CartItem]): The cart items containing the product.
        order_items (list[OrderItem]): The order items containing the product.
    """
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
    """
    Represents a brand in the system.

    Attributes:
        id (int): The unique identifier for the brand.
        name (str): The name of the brand.
        products (list[Product]): The products associated with the brand.
    """
    __tablename__ = 'brands'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped["Product"] = relationship("Product", back_populates="brand")


class Category(Base):
    """
    Represents a category in the system.

    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category.
        products (list[Product]): The products associated with the category.
    """
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    products: Mapped["Product"] = relationship("Product", back_populates="category")


class Review(Base):
    """
    Represents a review for a product.

    Attributes:
        id (int): The unique identifier for the review.
        user_id (int): The ID of the user who wrote the review.
        product_id (int): The ID of the product being reviewed.
        rating (float): The rating given to the product.
        comment (str): The comment for the review.
        created_at (datetime): The date the review was created.
        user (User): The user who wrote the review.
        product (Product): The product being reviewed.
    """
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
    """
    Represents an item in a user's cart.

    Attributes:
        id (int): The unique identifier for the cart item.
        user_id (int): The ID of the user who added the item to the cart.
        product_id (int): The ID of the product in the cart.
        quantity (int): The quantity of the product in the cart.
        added_at (datetime): The date the item was added to the cart.
        user (User): The user who added the item to the cart.
        product (Product): The product in the cart.
    """
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)  # Timestamp aggiunto

    user: Mapped["User"] = relationship("User", back_populates="cart_items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")


class Order(Base):
    """
    Represents an order placed by a user.

    Attributes:
        id (int): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        created_at (datetime): The date the order was created.
        confirmed_at (datetime): The date the order was confirmed.
        total (float): The total amount of the order.
        status (str): The status of the order.
        user (User): The user who placed the order.
        order_items (list[OrderItem]): The items in the order.
        address_id (int): The ID of the address for the order.
        address (Address): The address for the order.
    """
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
        """
        Update the status of the order based on the time elapsed since confirmation.

        If the order is confirmed, it will be updated to "Shipped" after 2 days
        and to "Delivered" after 5 days.
        """
        if self.status == 'Confermato' and self.confirmed_at:
            # Aggiorna lo stato a "Spedito" dopo 2 giorni
            if datetime.utcnow() >= self.confirmed_at + timedelta(days=2):
                self.status = 'Spedito, consegna prevista entro 3 giorni'
            # Aggiorna lo stato a "Consegnato" dopo 5 giorni
            if datetime.utcnow() >= self.confirmed_at + timedelta(days=5):
                self.status = "Consegnato"


class OrderItem(Base):
    """
    Represents an item in an order.

    Attributes:
        id (int): The unique identifier for the order item.
        order_id (int): The ID of the order.
        product_id (int): The ID of the product in the order.
        quantity (int): The quantity of the product in the order.
        price (float): The price of the product in the order.
        order (Order): The order associated with the order item.
        product (Product): The product associated with the order item.
    """
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)  # Prezzo aggiunto

    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    product: Mapped["Product"] = relationship("Product")
