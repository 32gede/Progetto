from flask import Blueprint, render_template, request, redirect, session, url_for
from models import User, UserSeller, UserBuyer, Product, Brand, Category, Review, CartItem
from database import get_db_session
from functools import wraps
from flask_login import login_user, login_required, current_user, logout_user

main_routes = Blueprint('main', __name__)


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
        db_session = get_db_session()
        existing_user = db_session.query(User).filter_by(email=email).first()
        if not existing_user:
            new_user = User(
                email=email,
                role=role)
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


@main_routes.route('/products')
@login_required
@role_required('buyer', 'seller')
def view_products():
    db_session = get_db_session()
    products = db_session.query(Product).all()
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
        price = request.form['price']
        quantity = request.form['quantity']
        brand_id = request.form['brand_id']
        category_id = request.form['category_id']
        db_session = get_db_session()
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
        return redirect(url_for('main.view_products'))
    db_session = get_db_session()
    brands = db_session.query(Brand).all()
    categories = db_session.query(Category).all()
    return render_template('add_product.html', brands=brands, categories=categories)


@main_routes.route('/product/remove', methods=['GET', 'POST'])
@login_required
@role_required('seller')
def remove_product(product_id):
    db_session = get_db_session()
    product = db_session.query(Product).filter_by(id=product_id).first()
    if product and product.seller_id == current_user.id:
        db_session.delete(product)
        db_session.commit()
        return redirect(url_for('main.view_products'))
    return render_template('remove_product.html', error="Product doesn't exist or already deleted")


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
        product.price = request.form['price']
        product.quantity = request.form['quantity']
        product.brand_id = request.form['brand_id']
        product.category_id = request.form['category_id']
        db_session.commit()
        return redirect(url_for('main.view_product', product_id=product.id))
    brands = db_session.query(Brand).all()
    categories = db_session.query(Category).all()
    return render_template('edit_product.html', product=product, brands=brands, categories=categories)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('main.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@main_routes.route('/seller-dashboard')
@login_required
@role_required('seller')
def seller_dashboard():
    return render_template('seller_dashboard.html')


@main_routes.route('/buyer-dashboard')
@login_required
@role_required('buyer')
def buyer_dashboard():
    return render_template('buyer_dashboard.html')
