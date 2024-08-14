from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField,SubmitField
from wtforms.fields.simple import SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, ValidationError, Regexp, Email, EqualTo
import re
import bleach
from markupsafe import escape

'''
ALLOWED_TAGS = ['b', 'i', 'u', 'a', 'p', 'strong', 'em']  # Define allowed HTML tags for sanitization

        if self.value_type == 'string':
            if self.is_html:
                value = bleach.clean(value, tags=ALLOWED_TAGS, strip=True)
            value = value.strip()
            if len(value) < (self.min_value or 0) or len(value) > (self.max_value or 255):
                raise ValidationError(
                    f"{self.error_message}: Length should be between {self.min_value} and {self.max_value} characters.")
            if self.allowed_chars_pattern and not re.match(self.allowed_chars_pattern, value):
                raise ValidationError(f"{self.error_message}: Contains invalid characters.")
            field.data = value
'''


class ProductForm(FlaskForm):
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

    # Cambia SelectField a StringField per permettere l'input manuale
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
    avatar_choice = SelectField('Avatar', choices=[('1yOOHEp8xJx7S_vbZmRe5K3nbia1XMVL6', 'Avatar 1'), ('1A8BXdiu2XE7FaAz8NmtYTYL4zYyIRsD7', 'Avatar 2')])
    submit = SubmitField('Register')


class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[Optional(), Length(min=2, max=255)])
    address = StringField('Address', validators=[Optional(), Length(min=2, max=255)])
    avatar = FileField('Avatar', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Update Profile')