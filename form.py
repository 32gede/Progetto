from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, ValidationError
import re
import bleach
from markupsafe import escape

ALLOWED_TAGS = ['b', 'i', 'u', 'a', 'p', 'strong', 'em']  # Define allowed HTML tags for sanitization


class ValidateAndSanitize:
    def __init__(self, value_type='string', min_value=None, max_value=None, allowed_chars_pattern=None,
                 error_message="Invalid value", is_html=False):
        self.value_type = value_type
        self.min_value = min_value
        self.max_value = max_value
        self.allowed_chars_pattern = allowed_chars_pattern
        self.error_message = error_message
        self.is_html = is_html

    def __call__(self, form, field):
        value = field.data

        if value is None:
            raise ValidationError(f"{self.error_message}: Value cannot be None.")

        value = escape(value)

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

        elif self.value_type == 'int':
            try:
                int_value = int(value)
                if (self.min_value is not None and int_value < self.min_value) or (
                        self.max_value is not None and int_value > self.max_value):
                    raise ValidationError(self.error_message)
                field.data = int_value
            except ValueError:
                raise ValidationError(self.error_message)

        elif self.value_type == 'float':
            try:
                float_value = float(value)
                if (self.min_value is not None and float_value < self.min_value) or (
                        self.max_value is not None and float_value > self.max_value):
                    raise ValidationError(self.error_message)
                field.data = float_value
            except ValueError:
                raise ValidationError(self.error_message)

        else:
            raise ValidationError("Invalid value_type specified. Must be 'string', 'int', or 'float'.")


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[
        DataRequired(),
        ValidateAndSanitize(value_type='string', min_value=1, max_value=255, error_message='Invalid product name.',
                            is_html=True)
    ])
    description = TextAreaField('Description', validators=[
        ValidateAndSanitize(value_type='string', min_value=1, max_value=255,
                            error_message='Invalid product description.', is_html=True)
    ])
    price = DecimalField('Price', validators=[
        DataRequired(),
        NumberRange(min=0.01, max=1000000, message='Invalid price.'),
        ValidateAndSanitize(value_type='float', min_value=0.01, max_value=1000000, error_message='Invalid price.',
                            is_html=False)
    ])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, max=1000000, message='Invalid quantity.'),
        ValidateAndSanitize(value_type='int', min_value=1, max_value=1000000, error_message='Invalid quantity.',
                            is_html=False)
    ])
    brand_id = SelectField('Brand')
    category_id = SelectField('Category')
    new_brand_name = StringField('New Brand Name')
    new_category_name = StringField('New Category Name')
    seller_id = SelectField('Seller')