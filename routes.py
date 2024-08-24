from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from functools import wraps
from flask_login import login_user, login_required, current_user, logout_user
import os
from datetime import datetime
from collegamento_drive import carica_imm


# IMPORT FROM OTHER FILES #

from models import User, UserSeller, Product, Brand, Category, Review, CartItem, Order, OrderItem, Address
from database import get_db_session
from form import ProductForm, ProfileForm, RegistrationForm, LoginForm, ReviewForm, AddToCartForm, EditCartForm, \
    RemoveFromCartForm, ConfirmOrderForm, CheckoutForm, FilterCategoriesForm, FilterBrandsForm, SearchProductForm, \
    RemoveReviewForm

# DEFINE BLUEPRINT #

import logging

logging.basicConfig()
main_routes = Blueprint('main', __name__)

UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """
    Check if a file is allowed based on its extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_upload_folder():
    """
    Ensure that the upload folder exists. Create it if it does not exist.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def role_required(*roles):
    """
    Decorator to restrict access to routes based on user roles.

    Args:
        *roles: Variable length argument list of roles.

    Returns:
        function: The decorated function.
    """
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


# MAIN ROUTES #

@main_routes.route('/')
def index():
    """
    Route for the index page.

    Returns:
        str: Rendered template for the index page.
    """
    update_order_status()
    if current_user.is_authenticated:
        with get_db_session() as db_session:
            user = db_session.query(User).filter_by(id=current_user.id).first()
            db_session.expunge(user)  # Detach the user instance from the session
            products = db_session.query(Product).order_by(desc(Product.insert_date)).limit(5).all()
            return render_template('index.html', products=products, user=user)
    else:
        return redirect(url_for('main.login'))


# USER ROUTES #

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.

    Returns:
        str: Rendered template for the login page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            user = db_session.query(User).filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)  # This attaches the user to the session
                session['id'] = user.id
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                return render_template('login.html', form=form, error='Invalid email or password.')
    return render_template('login.html', form=form)


@main_routes.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Route for user registration.

    Returns:
        str: Rendered template for the registration page.
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        with get_db_session() as db_session:
            existing_user = db_session.query(User).filter_by(email=form.email.data).first()
            if not existing_user:
                try:
                    new_address = Address(
                        address=form.address.data,
                        city=form.city.data
                    )
                    db_session.add(new_address)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    flash(str(e), 'error')
                    return render_template('registration.html', form=form)

                try:
                    new_user = User(
                        name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        role=form.role.data,
                        address=new_address
                    )
                    new_user.password_hash = form.password.data
                    db_session.add(new_user)
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    flash(str(e), 'error')
                    return render_template('registration.html', form=form)

                try:
                    if form.role.data == "seller":
                        new_seller = UserSeller(id=new_user.id, seller_rating=0)
                        db_session.add(new_seller)
                        db_session.commit()
                except Exception as e:
                    db_session.rollback()
                    flash(str(e), 'error')
                    return render_template('registration.html', form=form)

                return redirect(url_for('main.login'))
            else:
                flash('User already exists.')
                return render_template('registration.html', form=form)
    else:
        print(form.errors)  # Print form errors

    return render_template('registration.html', form=form)


@main_routes.route('/check-username', methods=['POST'])
def check_username():
    """
    Route to check if a username already exists.

    Returns:
        json: JSON response indicating if the username exists.
    """
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
@role_required('buyer', 'seller')
def logout():
    """
    Route for user logout.

    Returns:
        str: Redirect to the index page.
    """
    logout_user()  # Log out the user
    session.pop('id', None)  # Clear the session
    return redirect(url_for('main.index'))


@main_routes.route('/profile', methods=['GET'])
@login_required
@role_required('buyer', 'seller')
def profile_view():
    """
    Route to view user profile.

    Returns:
        str: Rendered template for the profile page.
    """
    form = ProductForm()  # Create a form instance
    with get_db_session() as db_session:
        user = db_session.query(User).options(joinedload(User.address)).filter_by(id=current_user.id).first()

    # Check if user exists and render the template accordingly
    if not user:
        return render_template('profile.html', error="No user found.", form=form)

    return render_template('profile.html', user=user, form=form)


@main_routes.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@role_required('buyer', 'seller')
def edit_profile():
    """
    Route to edit user profile.

    Returns:
        str: Rendered template for the edit profile page.
    """
    with get_db_session() as db_session:
        # Retrieve the current user
        user = db_session.query(User).filter_by(id=current_user.id).first()

        # Prepopulate the form with the user's data
        form = ProfileForm(obj=user)

        if form.validate_on_submit():
            # Process the avatar image upload
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
                    db_session.rollback()
                    flash(f'Failed to update the profile: {e}', 'error')
            else:
                flash('Invalid file type.', 'error')

            # Update the user's information
            try:
                user.username = form.username.data
                user.name = form.name.data

                if user.address:
                    user.address.address = form.address.data
                    user.address.city = form.city.data
                else:
                    new_address = Address(address=form.address.data, city=form.city.data)
                    db_session.add(new_address)
                    db_session.commit()

                    user.address = new_address

                db_session.commit()
                flash('Profile updated successfully!', 'success')
            except Exception as e:
                db_session.rollback()
                flash(f'Failed to update the profile: {e}', 'error')
            return profile_view()

        if user.address:
            form.address.data = user.address.address
            form.city.data = user.address.city

    return render_template('edit_profile.html', form=form)


# PRODUCT ROUTES #
@main_routes.route('/seller/products')
@login_required
@role_required('seller')
def view_products_seller():
    """
    Route to view products for sellers.

    Returns:
        str: Rendered template for the seller's products page.
    """
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
    """
    Route to view products for buyers.

    Returns:
        str: Rendered template for the buyer's products page.
    """
    form = SearchProductForm(request.args)
    with get_db_session() as db_session:
        products = db_session.query(Product).all()
        if not products:
            return render_template('products_buyer.html', error="No products available.", form=form)
        return render_template('products_buyer.html', products=products, form=form)


@main_routes.route('/products/<int:product_id>')
@login_required
@role_required('buyer', 'seller')
def view_product(product_id):
    """
    Route to view a specific product.

    Args:
        product_id (int): The ID of the product.

    Returns:
        str: Rendered template for the product page.
    """
    form = ProductForm()  # Create a form instance
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product:
            return render_template('product.html', error="Product not found.", form=form)
        return render_template('product.html', product=product, form=form)


@main_routes.route('/product/add', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def add_product():
    """
    Route to add a new product.

    Returns:
        str: Rendered template for the add product page.
    """
    form = ProductForm()

    with get_db_session() as db_session:
        brands = db_session.query(Brand).all()
        categories = db_session.query(Category).all()

        if form.validate_on_submit():
            try:
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
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.add_product'))

            flash('Product added successfully!', 'success')
            return redirect(url_for('main.view_products_seller'))

    return render_template('add_product.html', form=form, brands=brands, categories=categories)


@main_routes.route('/remove_product/<int:product_id>', methods=['POST'])
@login_required
@role_required('seller')
def remove_product(product_id):
    """
    Route to remove a product.

    Args:
        product_id (int): The ID of the product.

    Returns:
        str: Redirect to the seller's products page.
    """
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            flash('Product not found.')
            return redirect(url_for('main.view_products_seller'))

        if product.seller_id != current_user.id:
            flash('Unauthorized action.')
            return redirect(url_for('main.view_products_seller'))

        try:
            db_session.delete(product)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('main.view_products_seller'))

        flash('Product deleted successfully.')
    return redirect(url_for('main.view_products_seller'))


@main_routes.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def edit_product(product_id):
    """
    Route to edit a product.

    Args:
        product_id (int): The ID of the product.

    Returns:
        str: Rendered template for the edit product page.
    """
    form = ProductForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product or product.seller_id != current_user.id:
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            try:
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
            except Exception as e:
                db_session.rollback()
                flash('Failed to upload image.', 'error')
                return redirect(url_for('main.edit_product', product_id=product.id))
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

        return render_template('edit_product.html', form=form, product=product, brand_name=brand_name,
                               category_name=category_name, brands=brands, categories=categories)


# REVIEW ROUTES #

@main_routes.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])
@login_required
@role_required('buyer', 'seller')
def view_reviews(product_id):
    """
    Route to view reviews for a product.

    Args:
        product_id (int): The ID of the product.

    Returns:
        str: Rendered template for the reviews page.
    """
    form = ReviewForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            try:
                new_review = Review(
                    product_id=product.id,
                    user_id=current_user.id,
                    rating=form.rating.data,
                    comment=form.comment.data
                )
                db_session.add(new_review)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.view_reviews', product_id=product.id))

            return redirect(url_for('main.view_reviews', product_id=product.id))

        reviews = sorted(product.reviews, key=lambda review: review.created_at,
                         reverse=True)  # Sort reviews by created_at
        return render_template('view_reviews.html', product=product, reviews=reviews, form=form)


@main_routes.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def add_review(product_id):
    """
    Route to add a review for a product.

    Args:
        product_id (int): The ID of the product.

    Returns:
        str: Rendered template for the add review page.
    """
    form = ReviewForm()
    with get_db_session() as db_session:
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not product:
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            try:
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
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.add_review', product_id=product.id))

            return redirect(url_for('main.view_product', product_id=product.id))

        return render_template('add_review.html', form=form, product=product)


@main_routes.route('/edit_review/<int:product_id>/<int:review_id>', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def edit_review(product_id, review_id):
    """
    Route to edit a review for a product.

    Args:
        product_id (int): The ID of the product.
        review_id (int): The ID of the review.

    Returns:
        Response: The rendered template for editing the review or a redirect response.
    """
    form = ReviewForm()
    with get_db_session() as db_session:
        review = db_session.query(Review).filter_by(id=review_id, user_id=current_user.id,
                                                    product_id=product_id).first()
        product = db_session.query(Product).filter_by(id=product_id).first()

        if not review:
            flash('Review not found.')
            return redirect(url_for('main.view_product', product_id=product.id))

        if form.validate_on_submit():
            try:
                review.rating = form.rating.data
                review.comment = form.comment.data

                # Update the seller's rating
                seller = product.seller
                seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
                seller_rating = sum(review.rating for review in seller_reviews) / len(seller_reviews)
                seller.seller_rating = seller_rating

                db_session.commit()
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.edit_review', product_id=product.id, review_id=review.id))

            flash('Review updated successfully.')
            return redirect(url_for('main.view_product', product_id=product.id))

        # Prepopulate the form with the review data
        form.rating.data = review.rating
        form.comment.data = review.comment

        # Pass the review to the template
        return render_template('edit_review.html', form=form, product=product, review=review)


@main_routes.route('/product/<int:product_id>/remove_review/<int:review_id>', methods=['POST'])
@login_required
@role_required('buyer', 'seller')
def remove_review(product_id, review_id):
    """
    Route to remove a review for a product.

    Args:
        product_id (int): The ID of the product.
        review_id (int): The ID of the review.

    Returns:
        Response: A redirect response to the product view.
    """
    with get_db_session() as db_session:
        try:
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

            # Update the seller's rating
            seller = product.seller
            seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
            if seller_reviews:
                seller_rating = sum(review.rating for review in seller_reviews) / len(seller_reviews)
            else:
                seller_rating = 0  # Set rating to 0 if there are no more reviews

            seller.seller_rating = seller_rating

            db_session.commit()
        except Exception as e:
            db_session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('main.view_product', product_id=product_id))

        flash('Review deleted successfully.')
    return redirect(url_for('main.view_product', product_id=product_id))


# CART AND ORDER ROUTES #

@main_routes.route('/cart')
@login_required
@role_required('buyer')
def cart():
    """
    Route to view the cart.

    Returns:
        Response: The rendered template for the cart.
    """
    form = EditCartForm()
    with get_db_session() as db_session:
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, cart_total=cart_total, form=form)


@main_routes.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@role_required('buyer')
def add_to_cart(product_id):
    """
    Route to add a product to the cart.

    Args:
        product_id (int): The ID of the product to add.

    Returns:
        Response: A redirect response to the cart or product view.
    """
    form = AddToCartForm()

    # Print form data and validation status for debugging
    print("Form Data:", form.data)
    print("Form Errors:", form.errors)

    if form.validate_on_submit():
        with get_db_session() as db_session:
            try:
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
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.view_products_buyer'))

            flash('Product added to cart.')
            return redirect(url_for('main.cart'))

    # If form validation fails, print the errors and redirect
    flash('Invalid form submission.')
    return redirect(url_for('main.view_products_buyer'))


@main_routes.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
@role_required('buyer')
def remove_from_cart(item_id):
    """
    Route to remove an item from the cart.

    Args:
        item_id (int): The ID of the cart item to remove.

    Returns:
        Response: A redirect response to the cart view.
    """
    form = RemoveFromCartForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            try:
                item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
                if item:
                    db_session.delete(item)
                    db_session.commit()
                    flash('Item removed from cart.')
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.cart'))

            flash('Item removed from cart.')
        return redirect(url_for('main.cart'))
    return render_template('cart.html', form=form)


@main_routes.route('/cart/edit/<int:item_id>', methods=['POST'])
@login_required
@role_required('buyer')
def edit_cart(item_id):
    """
    Route to edit the quantity of an item in the cart.

    Args:
        item_id (int): The ID of the cart item to edit.

    Returns:
        Response: A redirect response to the cart view.
    """
    form = EditCartForm()
    if form.validate_on_submit():
        new_quantity = form.new_quantity.data
        if not new_quantity:
            flash('Invalid quantity.')
            return redirect(url_for('main.cart'))

        with get_db_session() as db_session:
            try:
                item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
                if item:
                    item.quantity = new_quantity
                    db_session.commit()
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.cart'))

            flash('Cart updated.')
            return redirect(url_for('main.cart'))
    return render_template('cart.html', form=form)


@main_routes.route('/checkout', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def checkout():
    """
    Route to handle the checkout process.

    Returns:
        Response: The rendered template for checkout or a redirect response.
    """
    form = CheckoutForm()

    with get_db_session() as db_session:
        cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()

        if form.validate_on_submit():
            try:
                if not cart_items:
                    flash('Il carrello è vuoto.', 'danger')
                    return redirect(url_for('main.cart'))

                # Use the default address if no address is provided
                address = form.address.data or current_user.address.address
                city = form.city.data or current_user.address.city

                # Group cart items by seller
                items_by_seller = {}
                for item in cart_items:
                    seller_id = item.product.seller_id
                    if seller_id not in items_by_seller:
                        items_by_seller[seller_id] = []
                    items_by_seller[seller_id].append(item)

                # Create a separate order for each seller
                for seller_id, items in items_by_seller.items():
                    total = sum(item.product.price * item.quantity for item in items)

                    # Create a new order for this seller
                    new_order = Order(user_id=current_user.id, total=total, address_id=current_user.address.id)
                    db_session.add(new_order)
                    db_session.commit()

                    # Add items to the order, update inventory, and remove from cart
                    for item in items:
                        order_item = OrderItem(
                            order_id=new_order.id,
                            product_id=item.product_id,
                            quantity=item.quantity,
                            price=item.product.price
                        )
                        db_session.add(order_item)

                        # Update inventory
                        product = db_session.query(Product).filter_by(id=item.product_id).first()
                        if product.quantity < item.quantity:
                            flash('Quantità insufficiente per il prodotto: {}'.format(product.name), 'danger')
                            return redirect(url_for('main.cart'))
                        product.quantity -= item.quantity

                        db_session.delete(item)

                    db_session.commit()
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.cart'))

            flash('Ordine completato con successo!', 'success')
            return redirect(url_for('main.order_history'))  # Redirect to order history page

        user_buyer = db_session.query(User).filter_by(id=current_user.id).first()
        return render_template('checkout.html', cart_items=cart_items, user_buyer=user_buyer, form=form)


@main_routes.route('/complete_order', methods=['POST'])
@login_required
@role_required('buyer')
def complete_order():
    """
    Route to complete an order.

    Returns:
        Response: A redirect response to the order history view.
    """
    with get_db_session() as db_session:
        try:
            user_buyer = db_session.query(User).filter_by(id=current_user.id).first()
            cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()

            if not cart_items:
                flash('Il carrello è vuoto.', 'danger')
                return redirect(url_for('main.cart'))

            # Use the new address if provided, otherwise use the default address from the profile
            address_id = session.pop('new_address_id', None)
            if address_id:
                address = db_session.query(Address).filter_by(id=address_id).first()
            else:
                address = user_buyer.address

            # Group cart items by seller
            items_by_seller = {}
            for item in cart_items:
                seller_id = item.product.seller_id
                if seller_id not in items_by_seller:
                    items_by_seller[seller_id] = []
                items_by_seller[seller_id].append(item)

            # Create a separate order for each seller
            for seller_id, items in items_by_seller.items():
                total = sum(item.product.price * item.quantity for item in items)

                # Create a new order for this seller
                new_order = Order(user_id=current_user.id, total=total, address_id=address.id)
                db_session.add(new_order)
                db_session.commit()

                # Add items to the order, update inventory, and remove from cart
                for item in items:
                    order_item = OrderItem(order_id=new_order.id, product_id=item.product.id, quantity=item.quantity,
                                           price=item.product.price)
                    db_session.add(order_item)
                    db_session.delete(item)

            db_session.commit()
        except Exception as e:
            db_session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('main.cart'))

        flash('Ordine completato con successo!', 'success')
        return redirect(url_for('main.order_history'))


@main_routes.route('/update_address', methods=['POST'])
@login_required
@role_required('buyer')
def update_address():
    """
    Route to update the address during checkout.

    Returns:
        Response: A redirect response to the checkout view.
    """
    form = CheckoutForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            try:
                new_address = Address(address=form.address.data, city=form.city.data)
                db_session.add(new_address)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')

            session['new_address_id'] = new_address.id
    return redirect(url_for('main.checkout'))


@main_routes.route('/order_history')
@login_required
@role_required('buyer')
def order_history():
    """
    Route to view the order history.

    Returns:
        Response: The rendered template for order history.
    """
    with get_db_session() as db_session:
        try:
            # Retrieve the user's orders
            orders = db_session.query(Order).filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()

            # Update order status based on time
            for order in orders:
                order.update_status_based_on_time()

            db_session.commit()
        except Exception as e:
            db_session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('main.index'))

        # Load items for each order
        for order in orders:
            order.items = db_session.query(OrderItem).filter_by(order_id=order.id).all()

        # Assume estimated delivery time is 5 business days
        estimated_delivery_days = 5
        return render_template('order_history.html', orders=orders, estimated_delivery_days=estimated_delivery_days)


@main_routes.route('/seller/orders')
@login_required
@role_required('seller')
def manage_orders():
    """
    Route for sellers to manage their orders.

    Returns:
        Response: The rendered template for managing orders.
    """
    form = ConfirmOrderForm()
    with get_db_session() as db_session:
        seller = db_session.query(UserSeller).filter_by(id=current_user.seller.id).first()

        if seller:
            seller_products = [product.id for product in seller.products]
            orders = db_session.query(Order).join(OrderItem).filter(OrderItem.product_id.in_(seller_products)).order_by(
                Order.created_at.desc()).all()
        else:
            orders = []

        # Fetch the buyer's email for each order
        for order in orders:
            order.buyer_email = db_session.query(User.email).filter_by(id=order.user_id).scalar()

        return render_template('manage_orders.html', orders=orders, form=form)


@main_routes.route('/seller/orders/confirm/<int:order_id>', methods=['POST'])
@login_required
@role_required('seller')
def confirm_order(order_id):
    """
    Route to confirm an order.

    Args:
        order_id (int): The ID of the order to confirm.

    Returns:
        Response: A redirect response to the manage orders view.
    """
    form = ConfirmOrderForm()
    if form.validate_on_submit():
        with get_db_session() as db_session:
            try:
                order = db_session.query(Order).filter_by(id=order_id).first()
                if order and order.status == 'In attesa':
                    order.status = 'Confermato'
                    order.confirmed_at = datetime.utcnow()  # Ensure this field exists in your table
                    db_session.commit()
                    flash('Ordine confermato con successo.', 'success')
                else:
                    flash('Impossibile confermare l\'ordine.', 'danger')
            except Exception as e:
                db_session.rollback()
                flash(str(e), 'error')
                return redirect(url_for('main.manage_orders'))
        return redirect(url_for('main.manage_orders'))


def update_order_status():
    """
    Update the status of all orders based on time.

    This function retrieves all orders from the database and updates their status
    based on the elapsed time since their creation.
    """
    with get_db_session() as db_session:
        try:
            orders = db_session.query(Order).all()  # Retrieve all orders
            for order in orders:
                order.update_status_based_on_time()
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            flash(str(e), 'error')


# SEARCH AND FILTER ROUTES #

@main_routes.route('/products', methods=['GET'])
@login_required
@role_required('buyer')
def search_product():
    """
    Route to search for products.

    This route handles the search functionality for products based on various filters
    such as name, description, price range, brand, and category.

    Returns:
        Response: The rendered template for the buyer's products page with the search results.
    """
    form = SearchProductForm(request.args)  # Create the form instance with request arguments

    if form.validate():
        with get_db_session() as db_session:
            products = search_products(
                db_session,
                form.name.data,
                form.description.data,
                form.min_price.data,
                form.max_price.data,
                form.brand_name.data,
                form.category_name.data
            )
            brands = db_session.query(Brand).all()
            categories = db_session.query(Category).all()

            return render_template(
                'products_buyer.html',
                products=products,
                brands=brands,
                categories=categories,
                form=form  # Pass the form to the template
            )
    else:
        # If the form is not valid, redirect or handle the error accordingly
        flash('Invalid search parameters.', 'danger')
        return redirect(url_for('main.index'))


@main_routes.route('/filter_brands', methods=['GET'])
@login_required
@role_required('buyer')
def filter_brands():
    """
    Route to filter brands based on a search term.

    This route handles the filtering of brands by a search term provided by the user.

    Returns:
        json: JSON response containing the list of brand names that match the search term.
    """
    form = FilterBrandsForm(request.args)
    if form.validate():
        with get_db_session() as db_session:
            brands = db_session.query(Brand).filter(Brand.name.ilike(f'%{form.search_term.data}%')).all()
            return jsonify([brand.name for brand in brands])
    else:
        return jsonify({'error': 'Invalid search term'}), 400


@main_routes.route('/filter_categories', methods=['GET'])
@login_required
@role_required('buyer')
def filter_categories():
    """
    Route to filter categories based on a search term.

    This route handles the filtering of categories by a search term provided by the user.

    Returns:
        json: JSON response containing the list of category names that match the search term.
    """
    form = FilterCategoriesForm(request.args)
    if form.validate():
        with get_db_session() as db_session:
            categories = db_session.query(Category).filter(Category.name.ilike(f'%{form.search_term.data}%')).all()
            return jsonify([category.name for category in categories])
    else:
        return jsonify({'error': 'Invalid search term'}), 400


def search_products(db_session, name, description, min_price, max_price, brand_name, category_name):
    """
    Search for products based on various filters.

    Args:
        db_session (Session): The database session.
        name (str): The name of the product.
        description (str): The description of the product.
        min_price (float): The minimum price of the product.
        max_price (float): The maximum price of the product.
        brand_name (str): The name of the brand.
        category_name (str): The name of the category.

    Returns:
        list: A list of products that match the search criteria.
    """
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
