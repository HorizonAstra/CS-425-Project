'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('I am a', choices=[('agent','Agent'),('renter','Renter')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddressForm(FlaskForm):
    street = StringField('Street')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('ZIP Code')
    submit = SubmitField('Save')

class CreditCardForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(), Length(max=20)])
    exp_date = DateField('Expiry Date', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    billing_address = SelectField('Billing Address', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

class PropertyForm(FlaskForm):
    property_type = SelectField('Type', choices=[('house','House'),('apartment','Apartment'),('commercial','Commercial')], validators=[DataRequired()])
    street = StringField('Street')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State')
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    available_from = DateField('Available From', validators=[DataRequired()])
    available_to = DateField('Available To', validators=[DataRequired()])
    sqr_footage = IntegerField('Square Footage')
    description = TextAreaField('Description')
    num_rooms = IntegerField('Rooms')
    building_type = StringField('Building Type')
    business_type = StringField('Business Type')
    submit = SubmitField('Save')

class SearchForm(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    min_bedrooms = IntegerField('Min Bedrooms')
    min_price = DecimalField('Min Price')
    max_price = DecimalField('Max Price')
    property_type = SelectField('Type', choices=[('', 'Any'),('house','House'),('apartment','Apartment'),('commercial','Commercial')])
    order_by = SelectField('Order by', choices=[('price','Price'),('rooms','Bedrooms')])
    submit = SubmitField('Search')

class BookingForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    card_number = SelectField('Payment Method', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Book')
'''














from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField,
    DecimalField, DateField, IntegerField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo,
    NumberRange, Optional                    # ← added Optional
)

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    email     = StringField('Email',      validators=[DataRequired(), Email(), Length(max=100)])
    password  = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm   = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('I am a',
                            choices=[('agent', 'Agent'), ('renter', 'Renter')],
                            validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email    = StringField('Email',    validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Login')


class AddressForm(FlaskForm):
    street   = StringField('Street')
    city     = StringField('City')
    state    = StringField('State')
    zip_code = StringField('ZIP Code')
    submit   = SubmitField('Save')


class CreditCardForm(FlaskForm):
    card_number     = StringField('Card Number',  validators=[DataRequired(), Length(max=20)])
    exp_date        = DateField('Expiry Date',    validators=[DataRequired()])
    cvv             = StringField('CVV',          validators=[DataRequired(), Length(min=3, max=3)])
    billing_address = SelectField('Billing Address', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')


class PropertyForm(FlaskForm):
    property_type  = SelectField('Type',
                                 choices=[('house','House'),
                                          ('apartment','Apartment'),
                                          ('commercial','Commercial')],
                                 validators=[DataRequired()])
    street         = StringField('Street')
    city           = StringField('City', validators=[DataRequired()])
    state          = StringField('State')
    price          = DecimalField('Price',
                                  validators=[DataRequired(), NumberRange(min=0)])
    available_from = DateField('Available From', validators=[DataRequired()])
    available_to   = DateField('Available To',   validators=[DataRequired()])
    sqr_footage    = IntegerField('Square Footage')
    description    = TextAreaField('Description')

    # subtype fields
    num_rooms     = IntegerField('Rooms')
    building_type = StringField('Building Type')   # for apartments
    business_type = StringField('Business Type')   # for commercial

    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    location      = StringField('Location', validators=[DataRequired()])
    date          = DateField('Date',       validators=[DataRequired()])

    # -------- optional filters (Optional() lets blanks pass validation) --------
    min_bedrooms  = IntegerField('Min Bedrooms',
                                 validators=[Optional(), NumberRange(min=0)])
    min_price     = DecimalField('Min Price',
                                 validators=[Optional(), NumberRange(min=0)])
    max_price     = DecimalField('Max Price',
                                 validators=[Optional(), NumberRange(min=0)])

    property_type = SelectField('Type',
                                choices=[('', 'Any'),
                                         ('house','House'),
                                         ('apartment','Apartment'),
                                         ('commercial','Commercial')])
    order_by      = SelectField('Order by',
                                choices=[('price','Price'), ('rooms','Bedrooms')])
    submit = SubmitField('Search')


class BookingForm(FlaskForm):
    start_date  = DateField('Start Date', validators=[DataRequired()])
    end_date    = DateField('End Date',   validators=[DataRequired()])
    card_number = SelectField('Payment Method', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Book')
