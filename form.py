from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField, FloatField
from wtforms.fields.simple import SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, Email, EqualTo


class ProductForm(FlaskForm):
    """
    Form for adding or editing a product.

    Attributes:
        name (StringField): The name of the product.
        description (TextAreaField): The description of the product.
        price (DecimalField): The price of the product.
        quantity (IntegerField): The quantity of the product.
        brand_id (StringField): The brand of the product.
        category_id (StringField): The category of the product.
        image (FileField): The image of the product.
        submit (SubmitField): The submit button.
    """
    name = StringField('Name', validators=[
        DataRequired(message='Product name is required.'),
        Length(min=1, max=255, message='Product name must be between 1 and 255 characters.')
    ])

    description = TextAreaField('Description', validators=[
        DataRequired(message='Product description is required.'),
        Length(min=1, max=255, message='Product description must be between 1 and 255 characters.')
    ])

    price = DecimalField('Price', validators=[
        DataRequired(message='Price is required.'),
        NumberRange(min=0.01, max=1000000, message='Price must be between 0.01 and 1,000,000.')
    ])

    quantity = IntegerField('Quantity', validators=[
        DataRequired(message='Quantity is required.'),
        NumberRange(min=1, max=1000000, message='Quantity must be between 1 and 1,000,000.')
    ])

    brand_id = StringField('Brand', validators=[
        DataRequired(message='Enter or select a brand.')
    ])

    category_id = StringField('Category', validators=[
        DataRequired(message='Enter or select a category.')
    ])

    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])

    submit = SubmitField('Add Product')


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): The email of the user.
        password (PasswordField): The password of the user.
        submit (SubmitField): The submit button.
    """
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Invalid email address.'),
        Length(min=3, max=255, message='Email must be between 3 and 255 characters.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=1, max=128, message='Password must be between 1 and 128 characters.')
    ])
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        email (StringField): The email of the user.
        password (PasswordField): The password of the user.
        confirm_password (PasswordField): The password confirmation.
        role (SelectField): The role of the user (seller or buyer).
        name (StringField): The full name of the user.
        username (StringField): The username of the user.
        city (StringField): The city of the user.
        address (StringField): The address of the user.
        avatar_choice (SelectField): The avatar choice of the user.
        submit (SubmitField): The submit button.
    """
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Invalid email address.'),
        Length(min=3, max=255, message='Email must be between 3 and 255 characters.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=1, max=128, message='Password must be between 1 and 128 characters.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Password confirmation is required.'),
        EqualTo('password', message='Passwords must match.')
    ])
    role = SelectField('Role', choices=[('seller', 'Seller'), ('buyer', 'Buyer')], validators=[
        DataRequired(message='Role is required.')
    ])
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required.'),
        Length(min=2, max=255, message='Name must be between 2 and 255 characters.')
    ])
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=2, max=255, message='Username must be between 2 and 255 characters.')
    ])
    city = StringField('City', validators=[Optional(), Length(min=2, max=255)])
    address = StringField('Address', validators=[Optional(), Length(min=2, max=255)])
    avatar_choice = SelectField('Avatar',
                                choices=[('1yOOHEp8xJx7S_vbZmRe5K3nbia1XMVL6', 'Avatar 1'),
                                         ('1A8BXdiu2XE7FaAz8NmtYTYL4zYyIRsD7', 'Avatar 2')])
    submit = SubmitField('Register')


class ProfileForm(FlaskForm):
    """
    Form for updating user profile.

    Attributes:
        name (StringField): The full name of the user.
        username (StringField): The username of the user.
        city (StringField): The city of the user.
        address (StringField): The address of the user.
        avatar (FileField): The avatar of the user.
        submit (SubmitField): The submit button.
    """
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[Optional(), Length(min=2, max=255)])
    address = StringField('Address', validators=[Optional(), Length(min=2, max=255)])
    avatar = FileField('Avatar', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')


class ReviewForm(FlaskForm):
    """
    Form for submitting or editing a product review.

    Attributes:
        rating (FloatField): The rating of the product.
        comment (TextAreaField): The comment for the review.
        submit (SubmitField): The submit button.
    """
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=3000)])
    submit = SubmitField('Submit')


class RemoveReviewForm(FlaskForm):
    """
    Form for removing a product review.

    Attributes:
        submit (SubmitField): The submit button.
    """
    submit = SubmitField('Remove')


class AddToCartForm(FlaskForm):
    """
    Form for adding a product to the cart.

    Attributes:
        quantity (IntegerField): The quantity of the product to add.
        submit (SubmitField): The submit button.
    """
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, max=1000000, message='Invalid quantity.')
    ])
    submit = SubmitField('Add to Cart')


class EditCartForm(FlaskForm):
    """
    Form for editing the quantity of a product in the cart.

    Attributes:
        new_quantity (IntegerField): The new quantity of the product.
        submit (SubmitField): The submit button.
    """
    new_quantity = IntegerField('New Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, max=1000000, message='Invalid quantity.')
    ])
    submit = SubmitField('Update')


class RemoveFromCartForm(FlaskForm):
    """
    Form for removing a product from the cart.

    Attributes:
        submit (SubmitField): The submit button.
    """
    submit = SubmitField('Remove')


class ConfirmOrderForm(FlaskForm):
    """
    Form for confirming an order.

    Attributes:
        submit (SubmitField): The submit button.
    """
    submit = SubmitField('Confirm Order')


class CheckoutForm(FlaskForm):
    """
    Form for completing the checkout process.

    Attributes:
        address (StringField): The address for the order.
        city (StringField): The city for the order.
        submit (SubmitField): The submit button.
    """
    address = StringField('Address', validators=[DataRequired(message="Address is required.")])
    city = StringField('City', validators=[DataRequired(message="City is required.")])
    submit = SubmitField('Complete Order')


class SearchProductForm(FlaskForm):
    """
    Form for searching products.

    Attributes:
        name (StringField): The name of the product.
        description (StringField): The description of the product.
        min_price (FloatField): The minimum price of the product.
        max_price (FloatField): The maximum price of the product.
        brand_name (StringField): The brand name of the product.
        category_name (StringField): The category name of the product.
    """
    name = StringField('Name', validators=[Optional(), Length(max=255)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    min_price = FloatField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = FloatField('Max Price', validators=[Optional(), NumberRange(min=0)])
    brand_name = StringField('Brand Name', validators=[Optional(), Length(max=255)])
    category_name = StringField('Category Name', validators=[Optional(), Length(max=255)])


class FilterBrandsForm(FlaskForm):
    """
    Form for filtering brands.

    Attributes:
        search_term (StringField): The search term for filtering brands.
    """
    search_term = StringField('Search Term', validators=[Optional(), Length(max=255)])


class FilterCategoriesForm(FlaskForm):
    """
    Form for filtering categories.

    Attributes:
        search_term (StringField): The search term for filtering categories.
    """
    search_term = StringField('Search Term', validators=[Optional(), Length(max=255)])
