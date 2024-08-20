from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from markupsafe import escape
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from functools import wraps
from flask_login import login_user, login_required, current_user, logout_user
import os
import sys
import bleach
from bleach.sanitizer import ALLOWED_TAGS
import re
from datetime import datetime
from collegamento_drive import carica_imm
# IMPORT FROM OTHER FILES #

from models import User, UserSeller, UserBuyer, Product, Brand, Category, Review, CartItem, Order, OrderItem
from database import get_db_session
from search import search_products
from form import ProductForm, ProfileForm, RegistrationForm, LoginForm, ReviewForm, AddToCartForm, EditCartForm, \
    RemoveFromCartForm, ConfirmOrderForm, CheckoutForm

# DEFINE BLUEPRINT #
import logging

logging.basicConfig()
main_routes = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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
    with get_db_session() as db_session:
        products = db_session.query(Product).order_by(desc(Product.insert_date)).limit(5).all()
        return render_template('index.html', products=products)


# USER ROUTES #

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            user = db_session.query(User).filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                session['id'] = user.id
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                return render_template('login.html', form=form, error='Invalid email or password.')
    return render_template('login.html', form=form)


@main_routes.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    print("Form created")  # Debugging line

    if form.validate_on_submit():
        print("Form validated")  # Debugging line
        with get_db_session() as db_session:
            existing_user = db_session.query(User).filter_by(email=form.email.data).first()
            if not existing_user:
                new_user = User(
                    name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    role=form.role.data,
                    address=form.address.data,
                    city=form.city.data,
                    avatar=form.avatar_choice.data
                )
                new_user.password_hash = form.password.data  # Hash the password
                print("New user created")  # Debugging line
                db_session.add(new_user)
                db_session.commit()

                if form.role.data == "seller":
                    new_seller = UserSeller(id=new_user.id, seller_rating=0)
                    db_session.add(new_seller)
                elif form.role.data == "buyer":
                    new_buyer = UserBuyer(id=new_user.id, buyer_rating=0)
                    db_session.add(new_buyer)
                db_session.commit()
                print("User committed")  # Debugging line
                return redirect(url_for('main.login'))
            else:
                print("User already exists")  # Debugging line
                flash('User already exists.')
                return render_template('registration.html', form=form)
    else:
        print("Form not validated")  # Debugging line
        print(form.errors)  # Print form errors

    return render_template('registration.html', form=form)


@main_routes.route('/check-username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username')

    with get_db_session() as db_session:
        user = db_session.query(User).filter_by(username=username).first()
        if user:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})


@main_routes.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    session.pop('id', None)  # Clear the session
    return redirect(url_for('main.index'))


@main_routes.route('/profile', methods=['GET'])
@login_required
@role_required('buyer', 'seller')
def profile_view():
    return render_template('profile.html')


@main_routes.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@role_required('buyer', 'seller')
def edit_profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        with get_db_session() as db_session:
            user = db_session.query(User).filter_by(id=current_user.id).first()

            if user:
                # Process the file upload
                file = request.files.get('avatar')

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

                    try:
                        file.save(file_path)
                        user.avatar = carica_imm(file_path, filename)
                        db_session.commit()  # Ensure commit here to save avatar changes
                        flash('Your profile has been updated.', 'success')
                    except Exception as e:
                        db_session.rollback()  # Rollback in case of error
                        flash(f'Failed to update the profile: {e}', 'error')
                else:
                    flash('Invalid file type.', 'error')

                # Update user information
                try:
                    user.username = form.username.data
                    user.name = form.name.data
                    user.city = form.city.data
                    user.address = form.address.data
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    flash(f'Failed to update the profile: {e}', 'error')

    return render_template('edit_profile.html', form=form)


# PRODUCT ROUTES #
@main_routes.route('/seller/products')
@login_required
@role_required('seller')
def view_products_seller():
    form = ProductForm()  # Create a form instance
    with get_db_session() as db_session:
        products = db_session.query(Product).filter_by(seller_id=current_user.id).all()

    # Check if products exist and render the template accordingly
    if not products:
        return render_template('products_seller.html', error="No products found.", form=form)

    return render_template('products_seller.html', products=products, form=form)

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

    form = ProductForm()  # Create a form instance
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product:
            return render_template('product.html', error="Product not found.",form=form)
        return render_template('product.html', product=product, form=form)


@main_routes.route('/product/add', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def add_product():
    form = ProductForm()

    with get_db_session() as db_session:
        brands = db_session.query(Brand).all()
        categories = db_session.query(Category).all()

        if form.validate_on_submit():
            # Gestisci brand
            brand = db_session.query(Brand).filter_by(name=form.brand_id.data).first()
            if not brand:
                brand = Brand(name=form.brand_id.data)
                db_session.add(brand)
                db_session.commit()
            brand_id = brand.id

            # Gestisci categoria
            category = db_session.query(Category).filter_by(name=form.category_id.data).first()
            if not category:
                category = Category(name=form.category_id.data)
                db_session.add(category)
                db_session.commit()
            category_id = category.id

            # Gestisci l'immagine
            file = form.image.data
            image_id = '1tvBMvCFzeZ14Kcr7z3iZ0yS6QfQOCFzQ'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                try:
                    file.save(file_path)
                    image_id = carica_imm(file_path, filename)
                except Exception as e:
                    db_session.rollback()
                    flash('Failed to upload image.', 'error')
                    return redirect(url_for('main.add_product'))
            else:
                image_id = '1tvBMvCFzeZ14Kcr7z3iZ0yS6QfQOCFzQ'  # Default image ID

            # Crea il prodotto
            new_product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                quantity=form.quantity.data,
                brand_id=brand_id,
                category_id=category_id,
                seller_id=current_user.id,
                image=image_id
            )
            db_session.add(new_product)
            db_session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('main.view_products_seller'))

    return render_template('add_product.html', form=form, brands=brands, categories=categories)


@main_routes.route('/remove_product/<int:product_id>', methods=['POST'])
@login_required
def remove_product(product_id):
    form = ProductForm()

    if form.validate_on_submit():
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
    else:
        flash('Invalid form submission.')
        return redirect(url_for('main.view_products_seller'))


@main_routes.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def edit_product(product_id):
    form = ProductForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product or product.seller_id != current_user.id:
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            product.quantity = form.quantity.data

            # Update brand and category names
            brand = db_session.query(Brand).filter_by(id=product.brand_id).first()
            category = db_session.query(Category).filter_by(id=product.category_id).first()
            if brand:
                brand.name = form.brand_id.data
            if category:
                category.name = form.category_id.data

            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                try:
                    file.save(file_path)
                    product.image = carica_imm(file_path, filename)
                except Exception as e:
                    db_session.rollback()
                    flash('Failed to upload image.', 'error')
                    return redirect(url_for('main.edit_product', product_id=product.id))

            db_session.commit()
            flash('Product updated successfully.', 'success')
            return redirect(url_for('main.view_product', product_id=product.id))

        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.quantity.data = product.quantity

        brand_name = db_session.query(Brand).filter_by(id=product.brand_id).first().name
        category_name = db_session.query(Category).filter_by(id=product.category_id).first().name

        form.brand_id.data = brand_name
        form.category_id.data = category_name

        brands = db_session.query(Brand).all()
        categories = db_session.query(Category).all()

        return render_template('edit_product.html', form=form, product=product, brand_name=brand_name, category_name=category_name, brands=brands, categories=categories)


# REVIEW ROUTES #

@main_routes.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])
@login_required
@role_required('buyer', 'seller')
def view_reviews(product_id):
    form = ReviewForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            new_review = Review(
                product_id=product.id,
                user_id=current_user.id,
                rating=form.rating.data,
                comment=form.comment.data
            )
            db_session.add(new_review)
            db_session.commit()
            return redirect(url_for('main.view_reviews', product_id=product.id))

        reviews = sorted(product.reviews, key=lambda review: review.created_at, reverse=True)  # Sort reviews by created_at
        return render_template('view_reviews.html', product=product, reviews=reviews, form=form)


@main_routes.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def add_review(product_id):
    form = ReviewForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            new_review = Review(
                product_id=product.id,
                user_id=current_user.id,
                rating=form.rating.data,
                comment=form.comment.data
            )
            db_session.add(new_review)
            seller = product.seller
            seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
            seller_rating = sum(review.rating for review in seller_reviews) / len(seller_reviews)
            seller.seller_rating = seller_rating
            db_session.commit()

            return redirect(url_for('main.view_product', product_id=product.id))

        return render_template('add_review.html', form=form, product=product)

@main_routes.route('/edit_review/<int:product_id>/<int:review_id>', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def edit_review(product_id, review_id):
    form = ReviewForm()
    with get_db_session() as db_session:
        review = db_session.query(Review).filter_by(id=review_id, user_id=current_user.id, product_id=product_id).first()
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not review:
            flash('Review not found.')
            return redirect(url_for('main.view_product', product_id=product.id))

        if form.validate_on_submit():
            review.rating = form.rating.data
            review.comment = form.comment.data
            seller = product.seller
            seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
            seller_rating = sum(review.rating for review in seller_reviews) / len(seller_reviews)
            seller.seller_rating = seller_rating
            db_session.commit()
            flash('Review updated successfully.')
            return redirect(url_for('main.view_product', product_id=product.id))

        form.rating.data = review.rating
        form.comment.data = review.comment

        return render_template('edit_review.html', form=form, product=product)


@main_routes.route('/product/<int:product_id>/remove_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
@role_required('buyer', 'seller')
def remove_review(product_id, review_id):
    form = ReviewForm()
    if form.validate_on_submit():
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

    return render_template('remove_review.html', form=form)


# CART AND ORDER ROUTES #

@main_routes.route('/cart')
@login_required
@role_required('buyer')
def cart():
    form = EditCartForm()
    with get_db_session() as db_session:
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, cart_total=cart_total, form=form)


@main_routes.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@role_required('buyer')
def add_to_cart(product_id):
    form = AddToCartForm()

    # Print form data and validation status for debugging
    print("Form Data:", form.data)
    print("Form Errors:", form.errors)

    if form.validate_on_submit():
        with get_db_session() as db_session:
            product = db_session.query(Product).filter_by(id=product_id).first()
            if not product:
                flash('Product not found.')
                return redirect(url_for('main.view_products_buyer'))

            if product.quantity == 0:
                flash('Product out of stock.')
                return redirect(url_for('main.view_products_buyer'))

            quantity = form.quantity.data

            cart_item = db_session.query(CartItem).filter_by(product_id=product.id, user_id=current_user.id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
                db_session.add(cart_item)
            db_session.commit()
            flash('Product added to cart.')
            return redirect(url_for('main.cart'))

    # If form validation fails, print the errors and redirect
    flash('Invalid form submission.')
    return redirect(url_for('main.view_products_buyer'))


@main_routes.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
@role_required('buyer')
def remove_from_cart(item_id):
    form = RemoveFromCartForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
            if item:
                db_session.delete(item)
                db_session.commit()
                flash('Item removed from cart.')
        return redirect(url_for('main.cart'))
    return render_template('cart.html', form=form)


@main_routes.route('/cart/edit/<int:item_id>', methods=['POST'])
@login_required
@role_required('buyer')
def edit_cart(item_id):
    form = EditCartForm()
    if form.validate_on_submit():
        new_quantity = form.new_quantity.data
        if not new_quantity:
            flash('Invalid quantity.')
            return redirect(url_for('main.cart'))

        with get_db_session() as db_session:
            item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
            if item:
                item.quantity = new_quantity
                db_session.commit()
            flash('Cart updated.')
            return redirect(url_for('main.cart'))
    return render_template('cart.html', form=form)

@main_routes.route('/checkout', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def checkout():
    form = CheckoutForm()

    with get_db_session() as db_session:
        # Ottieni gli articoli del carrello dell'utente
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
        user_buyer = db_session.query(User).filter_by(id=current_user.id).first()

        if form.validate_on_submit():
            address = form.address.data
            city = form.city.data

            if not cart_items:
                flash('Il carrello è vuoto. Non puoi completare l\'ordine.', 'warning')
                return redirect(url_for('main.view_products_buyer'))

            # Raggruppa gli articoli del carrello per venditore
            items_by_seller = {}
            for item in cart_items:
                seller_id = item.product.seller_id
                if seller_id not in items_by_seller:
                    items_by_seller[seller_id] = []
                items_by_seller[seller_id].append(item)

            # Crea un ordine separato per ogni venditore
            for seller_id, items in items_by_seller.items():
                total = sum(item.product.price * item.quantity for item in items)

                # Crea un nuovo ordine per questo venditore
                new_order = Order(user_id=current_user.id, total=total)
                db_session.add(new_order)
                db_session.commit()

                # Aggiungi gli articoli all'ordine, aggiorna l'inventario e rimuovi dal carrello
                for item in items:
                    order_item = OrderItem(
                        order_id=new_order.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                    db_session.add(order_item)

                    # Aggiorna l'inventario
                    product = db_session.query(Product).filter_by(id=item.product_id).first()
                    if product.quantity < item.quantity:
                        flash('Quantità insufficiente per il prodotto: {}'.format(product.name), 'danger')
                        return redirect(url_for('main.cart'))
                    product.quantity -= item.quantity

                    db_session.delete(item)

            db_session.commit()
            flash('Ordine completato con successo!', 'success')
            return redirect(url_for('main.order_history'))  # Reindirizza alla pagina degli ordini

        return render_template('checkout.html', cart_items=cart_items, user_buyer=user_buyer, form=form)


@main_routes.route('/update_address', methods=['POST'])
@login_required
@role_required('buyer')
def update_address():
    form = CheckoutForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            user_buyer = db_session.query(UserBuyer).filter_by(id=current_user.id).first()
            if user_buyer:
                user_buyer.user.address = form.address.data
                user_buyer.user.city = form.city.data
                db_session.commit()
                flash('Indirizzo aggiornato con successo.', 'success')
            else:
                flash('Errore durante l\'aggiornamento dell\'indirizzo.', 'danger')
    return redirect(url_for('main.checkout'))

@main_routes.route('/order_history')
@login_required
@role_required('buyer')
def order_history():
    with get_db_session() as db_session:
        # Recupera gli ordini dell'utente
        orders = db_session.query(Order).filter_by(user_id=current_user.id).all()

        # Carica anche gli articoli per ciascun ordine
        for order in orders:
            order.items = db_session.query(OrderItem).filter_by(order_id=order.id).all()

        # Supponiamo che il tempo di spedizione stimato sia di 5 giorni lavorativi
        estimated_delivery_days = 5
        return render_template('order_history.html', orders=orders, estimated_delivery_days=estimated_delivery_days)


@main_routes.route('/seller/orders')
@login_required
@role_required('seller')
def manage_orders():
    form = ConfirmOrderForm()
    with get_db_session() as db_session:
        seller = db_session.query(UserSeller).filter_by(id=current_user.seller.id).first()

        if seller:
            seller_products = [product.id for product in seller.products]
            orders = db_session.query(Order).join(OrderItem).filter(OrderItem.product_id.in_(seller_products)).all()
        else:
            orders = []

        # Fetch the buyer's address and city for each order
        for order in orders:
            order.user = db_session.query(User).filter_by(id=order.user_id).first()

        # Aggiorna lo stato degli ordini
        update_order_status()

        return render_template('manage_orders.html', orders=orders, form=form)


@main_routes.route('/seller/orders/confirm/<int:order_id>', methods=['POST'])
@login_required
@role_required('seller')
def confirm_order(order_id):
    form = ConfirmOrderForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            order = db_session.query(Order).filter_by(id=order_id).first()
            if order and order.status == 'In attesa':
                order.status = 'Confermato'
                order.confirmed_at = datetime.utcnow()  # Assicurati di avere questo campo nella tua tabella
                db_session.commit()
                flash('Ordine confermato con successo.', 'success')
            else:
                flash('Impossibile confermare l\'ordine.', 'danger')
        return redirect(url_for('main.manage_orders'))


def update_order_status():
    with get_db_session() as db_session:
        orders = db_session.query(Order).all()  # Controlla tutti gli ordini
        for order in orders:
            order.update_status_based_on_time()
        db_session.commit()


@main_routes.route('/admin/update_orders', methods=['POST'])
@login_required
@role_required('admin')  # Assicurati che solo l'admin possa fare questo
def update_orders():
    update_order_status()
    flash('Stato degli ordini aggiornato con successo.', 'success')
    return redirect(url_for('main.manage_orders'))


# SEARCH AND FILTER ROUTES #

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
