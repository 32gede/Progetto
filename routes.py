from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from markupsafe import escape
from werkzeug.utils import secure_filename
from functools import wraps
from flask_login import login_user, login_required, current_user, logout_user
import os
import sys
import bleach
from bleach.sanitizer import ALLOWED_TAGS
import re

# IMPORT FROM OTHER FILES #

from models import User, UserSeller, UserBuyer, Product, Brand, Category, Review, CartItem, Order, OrderItem
from database import get_db_session
from search import search_products


# DEFINE BLUEPRINT #


main_routes = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# HELPER FUNCTIONS #


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id' not in session:
                return redirect(url_for('main.login'))

            with get_db_session() as db_session:
                user = db_session.query(User).filter_by(id=session['id']).first()
                if user.role not in roles:
                    return redirect(url_for('main.index'))
                return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_and_sanitize(value, value_type='string', min_value=None, max_value=None, allowed_chars_pattern=None,
                          error_message="Invalid value", is_html=False):
    """
    Validate and sanitize the input value based on the type and constraints provided.

    :param value: The input value to be validated and sanitized.
    :param value_type: Type of value ('string', 'int', 'float').
    :param min_value: Minimum acceptable value (used for 'int' and 'float').
    :param max_value: Maximum acceptable value (used for 'int' and 'float').
    :param allowed_chars_pattern: Regex pattern to validate string characters.
    :param error_message: Error message to be returned if validation fails.
    :param is_html: Whether to sanitize HTML content.
    :return: Validated and sanitized value.
    :raises ValueError: If the input value fails validation.
    """
    if value is None:
        if value_type in ['int', 'float']:
            return None
        else:
            raise ValueError(f"{error_message}: Value cannot be None.")

    value = escape(value)

    if value_type == 'string':
        # Sanitize HTML if required
        if is_html:
            value = bleach.clean(value, tags=ALLOWED_TAGS, strip=True)
        # Validate string length and allowed characters
        value = value.strip()
        if len(value) < (min_value or 0) or len(value) > (max_value or 255):
            raise ValueError(f"{error_message}: Length should be between {min_value} and {max_value} characters.")
        if allowed_chars_pattern and not re.match(allowed_chars_pattern, value):
            raise ValueError(f"{error_message}: Contains invalid characters.")
        return value

    elif value_type == 'int':
        # Validate and sanitize integer
        try:
            int_value = int(value)
            if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
                raise ValueError(error_message)
            return int_value
        except ValueError:
            raise ValueError(error_message)

    elif value_type == 'float':
        # Validate and sanitize float
        try:
            float_value = float(value)
            if (min_value is not None and float_value < min_value) or (
                    max_value is not None and float_value > max_value):
                raise ValueError(error_message)
            return float_value
        except ValueError:
            raise ValueError(error_message)

    else:
        raise ValueError("Invalid value_type specified. Must be 'string', 'int', or 'float'.")


# MAIN ROUTES #


@main_routes.route('/')
def index():
    return render_template('index.html')


# USER ROUTES #

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = validate_and_sanitize(
            request.form['email'],
            value_type='string',
            min_value=3,
            max_value=255,
            error_message='Invalid email address.',
            is_html=True
        )
        password = validate_and_sanitize(
            request.form['password'],
            value_type='string',
            min_value=1,
            max_value=128,
            error_message="Invalid password.",
            is_html=True
        )

        with get_db_session() as db_session:
            user = db_session.query(User).filter_by(email=email).first()
            if user and user.check_password(password):
                session['id'] = user.id
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                return render_template('login.html', error='Invalid email or password.')
    return render_template('login.html')


@main_routes.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = validate_and_sanitize(
            request.form['email'],
            value_type='string',
            min_value=3,
            max_value=255,
            error_message='Invalid email address.',
            is_html=True
        )
        password = validate_and_sanitize(
            request.form['password'],
            value_type='string',
            min_value=1,
            max_value=128,
            error_message="Invalid password.",
            is_html=True
        )
        role = validate_and_sanitize(
            request.form['role'],
            value_type='string',
            min_value=4,
            max_value=10,
            error_message='Invalid role.',
            is_html=True
        )
        avatar_choice = request.form['avatar_choice']
        print(avatar_choice)

        if role == 'buyer':
            city = validate_and_sanitize(
                request.form['city'],
                value_type='string',
                min_value=2,
                max_value=255,
                error_message='Invalid street.',
                is_html=True
            )
            address = validate_and_sanitize(
                request.form['address'],
                value_type='string',
                min_value=2,
                max_value=255,
                error_message='Invalid city.',
                is_html=True
            )
        with get_db_session() as db_session:
            existing_user = db_session.query(User).filter_by(email=email).first()
            if not existing_user:
                new_user = User(
                    email=email,
                    role=role,
                    avatar=avatar_choice
                )
                new_user.password_hash = password  # Hash the password
                db_session.add(new_user)
                db_session.commit()

                if role == "seller":
                    new_seller = UserSeller(id=new_user.id, seller_rating=0)
                    db_session.add(new_seller)
                elif role == "buyer":
                    new_buyer = UserBuyer(id=new_user.id, buyer_rating=0, city=city, address=address)
                    db_session.add(new_buyer)
                db_session.commit()
                return redirect(url_for('main.login'))
            return render_template('registration.html', error='User already exists.')
    return render_template('registration.html')


@main_routes.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    session.pop('id', None)  # Clear the session
    return redirect(url_for('main.index'))


import base64


@main_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    with get_db_session() as db_session:
        if request.method == 'POST':
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                file_data = file.read()
                current_user.avatar = file_data
                db_session.commit()
                print('Your profile has been updated.')
            else:
                print('Invalid file type.')
        return render_template('profile.html', avatar_data=None)


# PRODUCT ROUTES #

@main_routes.route('/seller/products')
@login_required
@role_required('seller')
def view_products_seller():
    with get_db_session() as db_session:
        products = db_session.query(Product).filter_by(seller_id=current_user.id).all()
        if not products:
            return render_template('products_seller.html', error="No products found.")
        return render_template('products_seller.html', products=products)


@main_routes.route('/buyer/products')
@login_required
@role_required('buyer')
def view_products_buyer():
    with get_db_session() as db_session:
        products = db_session.query(Product).all()
        if not products:
            return render_template('products_buyer.html', error="No products available.")
        return render_template('products_buyer.html', products=products)


@main_routes.route('/products/<int:product_id>')
@login_required
@role_required('buyer', 'seller')
def view_product(product_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product:
            return render_template('product.html', error="Product not found.")
        return render_template('product.html', product=product)


@main_routes.route('/product/add', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def add_product():
    if request.method == 'POST':
        name = validate_and_sanitize(
            request.form['name'],
            value_type='string',
            min_value=1,
            max_value=255,
            error_message='Invalid product name.',
            is_html=True
        )
        description = validate_and_sanitize(
            request.form['description'],
            value_type='string',
            min_value=1,
            max_value=255,
            error_message='Invalid product description.',
            is_html=True
        )
        price = validate_and_sanitize(
            request.form['price'],
            value_type='float',
            min_value=0.01,
            max_value=1000000,
            error_message='Invalid price.',
            is_html=True
        )
        quantity = validate_and_sanitize(
            request.form['quantity'],
            value_type='int',
            min_value=1,
            max_value=1000000,
            error_message='Invalid quantity.',
            is_html=True
        )
        brand_id = validate_and_sanitize(
            request.form['brand_id'],
            value_type='string',
            min_value=0,
            max_value=255,
            allowed_chars_pattern=r'^[a-zA-Z0-9 &]*$',
            error_message='Invalid brand name.',
            is_html=True
        )
        new_brand_name = validate_and_sanitize(
            request.form['new_brand_name'],
            value_type='string',
            min_value=0,
            max_value=255,
            allowed_chars_pattern=r'^[a-zA-Z0-9 &]*$',
            error_message='Invalid new brand name.',
            is_html=True
        )
        category_id = validate_and_sanitize(
            request.form['category_id'],
            value_type='string',
            min_value=0,
            max_value=255,
            allowed_chars_pattern=r'^[a-zA-Z0-9 &]*$',
            error_message='Invalid category name.',
            is_html=True
        )
        new_category_name = validate_and_sanitize(
            request.form['new_category_name'],
            value_type='string',
            min_value=0,
            max_value=255,
            allowed_chars_pattern=r'^[a-zA-Z0-9 &]*$',
            error_message='Invalid new category name.',
            is_html=True
        )

        with get_db_session() as db_session:
            if not name or not description:
                flash('Name and description are required.')
                return redirect(url_for('main.add_product'))

            if not brand_id and not new_brand_name:
                flash('Brand is required.')
                return redirect(url_for('main.add_product'))

            if not category_id and not new_category_name:
                flash('Category is required.')
                return redirect(url_for('main.add_product'))

            if not brand_id and new_brand_name:
                flash('Please select a brand from the list.')
                return redirect(url_for('main.add_product'))

            if not category_id and new_category_name:
                flash('Please select a category from the list.')
                return redirect(url_for('main.add_product'))

            if not brand_id and not new_brand_name:
                flash('Please provide a name for the new brand.')
                return redirect(url_for('main.add_product'))

            if not category_id and not new_category_name:
                flash('Please provide a name for the new category.')
                return redirect(url_for('main.add_product'))

            if brand_id == 'new' and new_brand_name:
                existing_brand = db_session.query(Brand).filter_by(name=new_brand_name).first()
                if existing_brand:
                    flash('Brand name already exists. Please provide a different name.')
                    return redirect(url_for('main.add_product'))
                new_brand = Brand(name=new_brand_name)
                db_session.add(new_brand)
                db_session.commit()
                brand_id = new_brand.id
            elif brand_id == 'new':
                flash('Please provide a name for the new brand.')
                return redirect(url_for('main.add_product'))

            if category_id == 'new' and new_category_name:
                existing_category = db_session.query(Category).filter_by(name=new_category_name).first()
                if existing_category:
                    flash('Category name already exists. Please provide a different name.')
                    return redirect(url_for('main.add_product'))
                new_category = Category(name=new_category_name)
                db_session.add(new_category)
                db_session.commit()
                category_id = new_category.id
            elif category_id == 'new':
                flash('Please provide a name for the new category.')
                return redirect(url_for('main.add_product'))

            new_product = Product(
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                brand_id=brand_id,
                category_id=category_id,
                seller_id=current_user.id
            )
            db_session.add(new_product)
            db_session.commit()
            return redirect(url_for('main.view_products_seller'))

    with get_db_session() as db_session:
        brands = db_session.query(Brand).all()
        categories = db_session.query(Category).all()
        return render_template('add_product.html', brands=brands, categories=categories)


@main_routes.route('/remove_product/<int:product_id>', methods=['POST'])
@login_required
def remove_product(product_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            flash('Product not found.')
            return redirect(url_for('main.view_products_seller'))

        if product.seller_id != current_user.id:
            flash('Unauthorized action.')
            return redirect(url_for('main.view_products_seller'))

        db_session.delete(product)
        db_session.commit()
        flash('Product deleted successfully.')
        return redirect(url_for('main.view_products_seller'))


@main_routes.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def edit_product(product_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product or product.seller_id != current_user.id:
            return redirect(url_for('main.index'))

        if request.method == 'POST':
            name = validate_and_sanitize(
                request.form.get('name'),
                value_type='string',
                min_value=1,
                max_value=255,
                error_message='Invalid product name.',
                is_html=True
            )
            description = validate_and_sanitize(
                request.form.get('description'),
                value_type='string',
                min_value=1,
                max_value=255,
                error_message='Invalid product description.',
                is_html=True
            )
            price = validate_and_sanitize(
                request.form.get('price'),
                value_type='float',
                min_value=0.01,
                max_value=1000000,
                error_message='Invalid price.',
                is_html=True
            )
            quantity = validate_and_sanitize(
                request.form.get('quantity'),
                value_type='int',
                min_value=1,
                max_value=1000000,
                error_message='Invalid quantity.',
                is_html=True
            )
            brand_id = validate_and_sanitize(
                request.form.get('brand_id'),
                value_type='string',
                min_value=1,
                max_value=255,
                error_message='Invalid brand name.',
                is_html=True
            )
            category_id = validate_and_sanitize(
                request.form.get('category_id'),
                value_type='string',
                min_value=1,
                max_value=255,
                error_message='Invalid category name.',
                is_html=True
            )
            db_session.commit()
            return redirect(url_for('main.view_product', product_id=product.id))

        brands = db_session.query(Brand).all()
        categories = db_session.query(Category).all()
        return render_template('edit_product.html', product=product, brands=brands, categories=categories)


# REVIEW ROUTES #

@main_routes.route('/product/<int:product_id>/reviews')
@login_required
@role_required('buyer', 'seller')
def view_reviews(product_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            return redirect(url_for('main.index'))

        reviews = product.reviews  # Directly access the reviews attribute
        return render_template('view_reviews.html', product=product, reviews=reviews)


@main_routes.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def add_review(product_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            return redirect(url_for('main.index'))

        if request.method == 'POST':
            rating = validate_and_sanitize(
                request.form.get('rating'),
                value_type='float',
                min_value=0,
                max_value=5,
                error_message='Invalid rating.',
                is_html=True
            )
            comment = validate_and_sanitize(
                request.form.get('comment'),
                value_type='string',
                min_value=1,
                max_value=255,
                error_message='Invalid comment.',
                is_html=True
            )

            if not rating or not comment:
                flash('Please provide a rating and a review text.')
                return redirect(url_for('main.view_product', product_id=product.id))

            new_review = Review(
                product_id=product.id,
                user_id=current_user.id,
                rating=rating,
                comment=comment)
            db_session.add(new_review)
            seller = product.seller
            seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
            seller_rating = sum(review.rating for review in seller_reviews) / len(seller_reviews)
            seller.seller_rating = seller_rating
            db_session.commit()

            return redirect(url_for('main.view_product', product_id=product.id))

        return render_template('add_review.html', product=product)


@main_routes.route('/edit_review/<int:product_id>/<int:review_id>', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def edit_review(product_id, review_id):
    with get_db_session() as db_session:
        review = db_session.query(Review).filter_by(id=review_id,
                                                    user_id=current_user.id,
                                                    product_id=product_id).first()
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not review:
            flash('Review not found.')
            return redirect(url_for('main.view_product', product_id=product.id))

        if request.method == 'POST':
            rating = validate_and_sanitize(
                request.form.get('rating'),
                value_type='float',
                min_value=0,
                max_value=5,
                error_message='Invalid rating.',
                is_html=True
            )
            comment = validate_and_sanitize(
                request.form.get('comment'),
                value_type='string',
                min_value=1,
                max_value=255,
                error_message='Invalid comment.',
                is_html=True
            )

            if not rating or not comment:
                flash('Rating and comment are required.')
                return redirect(url_for('main.edit_review', product_id=product.id, review_id=review_id))

            review.rating = rating
            review.comment = comment
            seller = product.seller
            seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()

            seller_rating = sum(review.rating for review in seller_reviews) / len(seller_reviews)
            seller.seller_rating = seller_rating

            db_session.commit()
            flash('Review updated successfully.')
            return redirect(url_for('main.view_product', product_id=product.id))

        return render_template('edit_review.html', review=review, product=product)


@main_routes.route('/product/<int:product_id>/remove_review/<int:review_id>', methods=['POST'])
@login_required
@role_required('buyer', 'seller')
def remove_review(product_id, review_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            flash('Product not found.')
            return redirect(url_for('main.view_product', product_id=product_id))

        review = db_session.query(Review).filter_by(id=review_id).first()

        if not review:
            flash('Review not found.')
            return redirect(url_for('main.view_product', product_id=product_id))

        if review.user_id != current_user.id and product.seller_id != current_user.id:
            flash('Unauthorized action.')
            return redirect(url_for('main.view_product', product_id=product_id))

        db_session.delete(review)

        # Update seller's rating
        seller = product.seller
        seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
        seller_rating = sum(r.rating for r in seller_reviews) / len(seller_reviews)
        seller.seller_rating = seller_rating

        db_session.commit()
        flash('Review deleted successfully.')
        return redirect(url_for('main.view_product', product_id=product_id))


# CART AND ORDER ROUTES #

@main_routes.route('/cart')
@login_required
@role_required('buyer')
def cart():
    with get_db_session() as db_session:
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)


@main_routes.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@role_required('buyer')
def add_to_cart(product_id):
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product:
            flash('Product not found.')
            return redirect(url_for('main.view_products_buyer'))

        if product.quantity == 0:
            flash('Product out of stock.')
            return redirect(url_for('main.view_products_buyer'))

        quantity = validate_and_sanitize(
            request.form.get('quantity'),
            value_type='int',
            min_value=1,
            max_value=1000000,
            error_message='Invalid quantity.',
            is_html=True
        )

        cart_item = db_session.query(CartItem).filter_by(product_id=product.id, user_id=current_user.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(user_id=current_user.id,
                                 product_id=product.id,
                                 quantity=quantity)
            db_session.add(cart_item)
        db_session.commit()
        flash('Product added to cart.')
        return redirect(url_for('main.cart'))


@main_routes.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
@role_required('buyer')
def remove_from_cart(item_id):
    with get_db_session() as db_session:
        item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
        if item:
            db_session.delete(item)
            db_session.commit()
            flash('Item removed from cart.')
        return redirect(url_for('main.cart'))


@main_routes.route('/cart/edit', methods=['POST'])
@login_required
@role_required('buyer')
def edit_cart():
    item_id = validate_and_sanitize(
        request.form.get('item_id'),
        value_type='int',
        min_value=1,
        error_message="Invalid item ID.",
        is_html=True
    )
    new_quantity = validate_and_sanitize(
        request.form.get('new_quantity'),
        value_type='int',
        min_value=1,
        max_value=1000000,
        error_message='Invalid quantity.',
        is_html=True
    )
    if not item_id or not new_quantity:
        flash('Invalid item ID or quantity.')
        return redirect(url_for('main.cart'))

    with get_db_session() as db_session:
        item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
        if item:
            item.quantity = new_quantity
            db_session.commit()
        flash('Cart updated.')
        return redirect(url_for('main.cart'))


@main_routes.route('/order_history')
@login_required
@role_required('buyer')
def order_history():
    with get_db_session() as db_session:
        # Recupera gli ordini dell'utente
        orders = db_session.query(Order).filter_by(user_id=current_user.id).all()

        # Supponiamo che il tempo di spedizione stimato sia di 5 giorni lavorativi
        estimated_delivery_days = 5

        return render_template('order_history.html', orders=orders, estimated_delivery_days=estimated_delivery_days)


@main_routes.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    with get_db_session() as db_session:
        # Ottieni gli articoli del carrello dell'utente
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()

        # Recupera l'indirizzo dell'utente
        user_buyer = db_session.query(UserBuyer).filter_by(id=current_user.id).first()

        if request.method == 'POST':
            if not cart_items:
                flash('Il carrello è vuoto. Non puoi completare l\'ordine.', 'warning')
                return redirect(url_for('main.view_products_buyer'))

            # Calcola il totale dell'ordine
            total = sum(item.product.price * item.quantity for item in cart_items)

            # Crea un nuovo ordine
            new_order = Order(user_id=current_user.id, total=total)
            db_session.add(new_order)
            db_session.commit()

            # Aggiungi gli articoli all'ordine e rimuovi dal carrello
            for item in cart_items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.product.price  # Assicurati di passare il prezzo qui
                )
                db_session.add(order_item)

                # Rimuovi l'item dal carrello
                db_session.delete(item)

            db_session.commit()
            flash('Ordine completato con successo!', 'success')
            return redirect(url_for('main.order_history'))  # Reindirizza alla pagina degli ordini

        return render_template('checkout.html', cart_items=cart_items, user_buyer=user_buyer)







@main_routes.route('/products', methods=['GET'])
@login_required
@role_required('buyer')
def search_product():
    with get_db_session() as db_session:
        query = validate_and_sanitize(
            request.args.get('query', ''),
            value_type='string',
            min_value=0,
            max_value=255,
            error_message='Invalid search query.',
            is_html=True
        )
        name = validate_and_sanitize(
            request.args.get('name', ''),
            value_type='string',
            min_value=0,
            max_value=255,
            error_message='Invalid product name.',
            is_html=True
        )
        description = validate_and_sanitize(
            request.args.get('description', ''),
            value_type='string',
            min_value=0,
            max_value=255,
            error_message='Invalid product description.',
            is_html=True
        )
        min_price = validate_and_sanitize(
            request.args.get('min_price', type=float),
            value_type='float',
            min_value=0,
            max_value=1000000,
            error_message='Invalid minimum price.',
            is_html=True
        )
        max_price = validate_and_sanitize(
            request.args.get('max_price', type=float),
            value_type='float',
            min_value=0,
            max_value=1000000,
            error_message='Invalid maximum price.',
            is_html=True
        )
        brand_name = validate_and_sanitize(
            request.args.get('brand_name', ''),
            value_type='string',
            min_value=0,
            max_value=255,
            error_message='Invalid brand name.',
            is_html=True
        )
        category_name = validate_and_sanitize(
            request.args.get('category_name', ''),
            value_type='string',
            min_value=0,
            max_value=255,
            error_message='Invalid category name.',
            is_html=True
        )

        products = search_products(
            db_session,
            name,
            description,
            min_price,
            max_price,
            brand_name,
            category_name)
        brands = db_session.query(Brand).all()
        categories = db_session.query(Category).all()

        return render_template('products_buyer.html', products=products, brands=brands, categories=categories,
                               selected_brand=brand_name, selected_category=category_name)


@main_routes.route('/filter_brands', methods=['GET'])
@login_required
@role_required('buyer')
def filter_brands():
    with get_db_session() as db_session:
        search_term = validate_and_sanitize(
            request.args.get('search_term', ''),
            value_type='string',
            min_value=0,
            max_value=255,
            error_message='Invalid search term.',
            is_html=True
        )
        brands = db_session.query(Brand).filter(Brand.name.ilike(f'%{search_term}%')).all()
        return jsonify([brand.name for brand in brands])


@main_routes.route('/filter_categories', methods=['GET'])
@login_required
@role_required('buyer')
def filter_categories():
    with get_db_session() as db_session:
        search_term = validate_and_sanitize(
            request.args.get('search_term', ''),
            value_type='string',
            min_value=1,
            max_value=255,
            error_message='Invalid search term.',
            is_html=True
        )
        categories = db_session.query(Category).filter(Category.name.ilike(f'%{search_term}%')).all()
        return jsonify([category.name for category in categories])


'''
def order_history_returns_orders_for_valid_user(client, db_session, valid_user):
    response = client.get('/order_history', query_string={'user_id': valid_user.id})
    assert response.status_code == 200
    assert len(response.json['orders']) > 0

def order_history_returns_empty_for_user_with_no_orders(client, db_session, user_with_no_orders):
    response = client.get('/order_history', query_string={'user_id': user_with_no_orders.id})
    assert response.status_code == 200
    assert len(response.json['orders']) == 0

def order_history_returns_404_for_invalid_user(client, db_session):
    response = client.get('/order_history', query_string={'user_id': 9999})
    assert response.status_code == 404

def order_history_handles_missing_user_id(client, db_session):
    response = client.get('/order_history')

    assert response.status_code == 400
    assert response.json == {'error': 'Missing user_id parameter'}
'''
