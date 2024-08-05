import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy.testing import db
from werkzeug.utils import secure_filename
from models import User, UserSeller, UserBuyer, Product, Brand, Category, Review, CartItem, Order, OrderItem
from database import get_db_session
from functools import wraps
from flask_login import login_user, login_required, current_user, logout_user
from hashlib import md5


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

@main_routes.route('/')
def index():
    if 'id' in session:
        print(session['id'])
    else:
        print('NESSUN cookie')
    return render_template('index.html')

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

@main_routes.route('/cart')
@login_required
@role_required('buyer')
def cart():
    db_session = get_db_session()
    cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)

@main_routes.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
@role_required('buyer')
def remove_from_cart(item_id):
    db_session = get_db_session()
    item = db_session.query(CartItem).filter_by(id=item_id, user_id=current_user.id).first()
    if item:
        db_session.delete(item)
        db_session.commit()
    return redirect(url_for('main.cart'))

@main_routes.route('/order_history')
@login_required
@role_required('buyer')
def order_history():
    db_session = get_db_session()
    orders = db_session.query(Order).filter_by(user_id=current_user.id).all()
    return render_template('order_history.html', orders=orders)

@main_routes.route('/checkout', methods=['POST'])
@login_required
@role_required('buyer')
def checkout():
    db_session = get_db_session()
    cart_items = db_session.query(CartItem).filter_by(user_id=current_user.id).all()
    if not cart_items:
        return redirect(url_for('main.cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)
    new_order = Order(user_id=current_user.id, total=total)
    db_session.add(new_order)
    db_session.commit()

    for item in cart_items:
        order_item = OrderItem(order_id=new_order.id, product_id=item.product.id, quantity=item.quantity)
        db_session.add(order_item)
        db_session.delete(item)

    db_session.commit()
    return redirect(url_for('main.order_history'))

@main_routes.route('/products')
@login_required
@role_required('seller')
def view_products_seller():
    db_session = get_db_session()
    products = db_session.query(Product).filter_by(seller_id=current_user.id).all()
    if not products:
        return render_template('products.html', error="You haven't added any products yet")
    return render_template('products.html', products=products)

@main_routes.route('/buyer/products')
@login_required
@role_required('buyer')
def view_products_buyer():
    db_session = get_db_session()
    products = db_session.query(Product).all()
    if not products:
        return render_template('products.html', error="There are no products available")
    return render_template('products.html', products=products)

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
            price = validate_int(request.form['price'],
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
    if not product or product.seller_id != session['id']:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        try:
            price = validate_int(request.form['price'],
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
        product.brand_id = request.form['brand_id']
        product.category_id = request.form['category_id']
        db_session.commit()
        return redirect(url_for('main.view_product', product_id=product.id))
    brands = db_session.query(Brand).all()
    categories = db_session.query(Category).all()
    return render_template('edit_product.html', product=product, brands=brands, categories=categories)



@main_routes.route('/buyer-dashboard')
@login_required
@role_required('buyer')
def buyer_dashboard():
    return render_template('buyer_dashboard.html')