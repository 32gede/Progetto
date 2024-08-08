from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from models import User, UserSeller, UserBuyer, Product, Brand, Category, Review, CartItem, Order, OrderItem
from database import get_db_session
from functools import wraps
from flask_login import login_user, login_required, current_user, logout_user
from hashlib import md5
import os
import sys

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
            db_session = get_db_session()
            user = db_session.query(User).filter_by(id=session['id']).first()
            if user.role not in roles:
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('main.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def validate_int(value, min_value=0, max_value=2147483647, error_message="Invalid value"):
    try:
        int_value = int(value)
        if int_value < min_value or int_value > max_value:
            raise ValueError(error_message)
        return int_value
    except ValueError:
        raise ValueError(error_message)


def validate_float(value, min_value=0, max_value=sys.float_info.max, error_message="Invalid value"):
    try:
        float_value = float(value)
        if float_value < min_value or float_value > max_value:
            raise ValueError(error_message)
        return float_value
    except ValueError:
        raise ValueError(error_message)


# MAIN ROUTES #


@main_routes.route('/')
def index():
    return render_template('index.html')


# USER ROUTES #


@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db_session = get_db_session()
        user = db_session.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            session['id'] = user.id
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@main_routes.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        avatar_choice = request.form['avatar_choice']
        db_session = get_db_session()
        existing_user = db_session.query(User).filter_by(email=email).first()
        if not existing_user:
            new_user = User(
                email=email,
                role=role,
                avatar=avatar_choice if avatar_choice else None
            )
            new_user.password_hash = password  # Hash the password
            db_session.add(new_user)
            db_session.commit()

            if role == "seller":
                new_seller = UserSeller(id=new_user.id, seller_rating=0)
                db_session.add(new_seller)
            elif role == "buyer":
                new_buyer = UserBuyer(id=new_user.id, buyer_rating=0)
                db_session.add(new_buyer)

            db_session.commit()
            return redirect(url_for('main.login'))
        return render_template('registration.html', error='User already exists')
    return render_template('registration.html')


@main_routes.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    session.pop('id', None)  # Clear the session
    return redirect(url_for('main.index'))


@main_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db_session = get_db_session()
    if request.method == 'POST':
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            ensure_upload_folder()  # Ensure the upload folder exists
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            current_user.avatar = filename
            db_session.commit()
            flash('Your profile has been updated.')
        else:
            flash('Invalid file type.')
    return render_template('profile.html')


# PRODUCT ROUTES #


@main_routes.route('/seller/products')
@login_required
@role_required('seller')
def view_products_seller():
    db_session = get_db_session()
    products = db_session.query(Product).filter_by(seller_id=current_user.id).all()
    if not products:
        return render_template('products_seller.html', error="You haven't added any products yet")
    return render_template('products_seller.html', products=products)


@main_routes.route('/buyer/products')
@login_required
@role_required('buyer')
def view_products_buyer():
    db_session = get_db_session()
    products = db_session.query(Product).all()
    if not products:
        return render_template('products_buyer.html', error="There are no products available")
    return render_template('products_buyer.html', products=products)


@main_routes.route('/products/<int:product_id>')
@login_required
@role_required('buyer', 'seller')
def view_product(product_id):
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()
    if not product:
        return render_template('product.html', error="Product doesn't exist")
    return render_template('product.html', product=product)


@main_routes.route('/product/add', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        try:
            price = validate_float(request.form['price'],
                                   error_message='Invalid price. Please enter a number between 0 and 2147483647')
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('main.add_product'))

        try:
            quantity = validate_int(request.form['quantity'],
                                    error_message='Invalid quantity. Please enter a number between 0 and 2147483647')
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('main.add_product'))

        brand_id = request.form['brand_id']
        new_brand_name = request.form.get('new_brand_name')
        category_id = request.form['category_id']
        new_category_name = request.form.get('new_category_name')

        db_session = get_db_session()

        if brand_id == 'new' and new_brand_name:
            new_brand = Brand(name=new_brand_name)
            db_session.add(new_brand)
            db_session.commit()
            brand_id = new_brand.id
        elif brand_id == 'new':
            flash('Please provide a name for the new brand.')
            return redirect(url_for('main.add_product'))

        if category_id == 'new' and new_category_name:
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

    db_session = get_db_session()
    brands = db_session.query(Brand).all()
    categories = db_session.query(Category).all()
    return render_template('add_product.html', brands=brands, categories=categories)


@main_routes.route('/remove_product/<int:product_id>', methods=['POST'])
@login_required
def remove_product(product_id):
    db_session = get_db_session()
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
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()

    if not product or product.seller_id != current_user.id:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']

        try:
            product.price = validate_float(request.form['price'],
                                           error_message='Invalid price. Please enter a number between 0 and 2147483647')
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('main.edit_product', product_id=product.id))

        try:
            product.quantity = validate_int(request.form['quantity'],
                                            error_message='Invalid quantity. Please enter a number between 0 and 2147483647')
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('main.edit_product', product_id=product.id))

        product.brand_id = request.form['brand_id']
        product.category_id = request.form['category_id']
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
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()

    if not product:
        return redirect(url_for('main.index'))

    reviews = product.reviews  # Directly access the reviews attribute
    return render_template('view_reviews.html', product=product, reviews=reviews)


@main_routes.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def add_review(product_id):
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()

    if not product:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if not rating or not comment:
            flash('Please provide a rating and a review text.')
            return redirect(url_for('main.view_product', product_id=product.id))

        try:
            rating = validate_float(rating, min_value=1, max_value=5,
                                    error_message='Invalid rating. Please enter a number between 1 and 5.')
        except ValueError as e:
            flash(str(e))
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
    db_session = get_db_session()
    review = db_session.query(Review).filter_by(id=review_id, user_id=current_user.id, product_id=product_id).first()
    product = db_session.query(Product).filter_by(id=product_id).first()
    if not review:
        flash('Review not found.')
        return redirect(url_for('main.view_product', product_id=product.id))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if not rating or not comment:
            flash('Rating and comment are required.')
            return redirect(url_for('main.edit_review', product_id=product.id, review_id=review_id))

        try:
            rating = validate_float(rating, min_value=1, max_value=5,
                                    error_message='Invalid rating. Please enter a number between 1 and 5.')
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('main.view_product', product_id=product.id))

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
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()

    if not product:
        flash('Product not found.')
        return redirect(url_for('main.view_reviews', product_id=product_id))

    review = db_session.query(Review).filter_by(id=review_id).first()

    if not review:
        flash('Review not found.')
        return redirect(url_for('main.view_reviews', product_id=product_id))

    if review.user_id != current_user.id and product.seller_id != current_user.id:
        flash('Unauthorized action.')
        return redirect(url_for('main.view_reviews', product_id=product_id))

    db_session.delete(review)

    # Update seller's rating
    seller = product.seller
    seller_reviews = db_session.query(Review).join(Product).filter(Product.seller_id == seller.id).all()
    seller_rating = sum(r.rating for r in seller_reviews) / len(seller_reviews)
    seller.seller_rating = seller_rating

    db_session.commit()
    flash('Review deleted successfully.')
    return redirect(url_for('main.view_reviews', product_id=product_id))


# CART AND ORDER ROUTES #


@main_routes.route('/cart')
@login_required
@role_required('buyer')
def cart():
    db_session = get_db_session()
    cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)


@main_routes.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@role_required('buyer')
def add_to_cart(product_id):
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()
    if not product:
        flash('Product not found.')
        return redirect(url_for('main.view_products_buyer'))

    if product.quantity == 0:
        flash('Product out of stock.')
        return redirect(url_for('main.view_products_buyer'))

    quantity = request.form.get('quantity')

    try:
        quantity = validate_int(quantity, min_value=1, max_value=product.quantity,
                                error_message=f'Invalid quantity. Please enter a number between 1 and {product.quantity}')
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('main.view_product', product_id=product.id))

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
    db_session = get_db_session()
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
    item_id = request.form.get('item_id')
    new_quantity = request.form.get('new_quantity')
    if not item_id or not new_quantity:
        flash('Invalid item ID or quantity')
        return redirect(url_for('main.cart'))

    try:
        new_quantity = validate_int(new_quantity, min_value=1,
                                    error_message='Invalid quantity. Please enter a number greater than 0')
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('main.cart'))

    db_session = get_db_session()
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
    db_session = get_db_session()
    orders = db_session.query(Order).filter_by(user_id=current_user.id).all()
    return render_template('order_history.html', orders=orders)


@main_routes.route('/checkout', methods=['GET', 'POST'])
@login_required
@role_required('buyer')
def checkout():
    db_session = get_db_session()
    cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('No items in cart.')
        return redirect(url_for('main.cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)
    new_order = Order(user_id=current_user.id, total=total)
    db_session.add(new_order)
    db_session.commit()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price)
        db_session.add(order_item)

        # Update product quantity
        product = db_session.query(Product).filter_by(id=item.product.id).first()
        if product:
            product.quantity -= item.quantity

        db_session.delete(item)

    db_session.commit()
    flash('Order placed successfully.')
    return redirect(url_for('main.order_history'))


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
