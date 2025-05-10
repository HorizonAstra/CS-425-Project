from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import foreign

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    email        = db.Column(db.String(100), primary_key=True)
    full_name    = db.Column(db.String(200), nullable=False)
    user_type    = db.Column(db.String(20), nullable=False)  # 'agent' or 'renter'
    password_hash= db.Column(db.String(128), nullable=False)

    agent    = db.relationship('Agent', backref='user', uselist=False)
    renter   = db.relationship('Renter', backref='user', uselist=False)
    addresses= db.relationship('Address', backref='user', cascade='all, delete-orphan')
    cards    = db.relationship(
        'CreditCard',
        primaryjoin="User.email == foreign(CreditCard.renter_email)",
        backref='renter',
        cascade='all, delete-orphan'
    )
    #bookings = db.relationship('Booking', backref='renter', cascade='all, delete-orphan')
    bookings = db.relationship(
    'Booking',
    primaryjoin="User.email == foreign(Booking.renter_email)",
    backref='renter',
    cascade='all, delete-orphan'
    )

    def get_id(self):
        return self.email


class Agent(db.Model):
    __tablename__ = 'agents'
    email        = db.Column(db.String(100), db.ForeignKey('users.email', ondelete='CASCADE'), primary_key=True)
    job_title    = db.Column(db.String(100))
    agency_name  = db.Column(db.String(100))
    contact_info = db.Column(db.String(255))
    properties   = db.relationship('Property', backref='agent', cascade='all, delete-orphan')


class Renter(db.Model):
    __tablename__ = 'renters'
    email              = db.Column(db.String(100), db.ForeignKey('users.email', ondelete='CASCADE'), primary_key=True)
    desired_move_in    = db.Column(db.Date)
    preferred_location = db.Column(db.String(255))
    budget             = db.Column(db.Numeric(12,2))


class Address(db.Model):
    __tablename__ = 'addresses'
    address_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('users.email', ondelete='CASCADE'), nullable=False)
    street     = db.Column(db.String(255))
    city       = db.Column(db.String(100))
    state      = db.Column(db.String(50))
    zip_code   = db.Column(db.String(20))
    cards      = db.relationship('CreditCard', backref='address')


class CreditCard(db.Model):
    __tablename__ = 'credit_cards'
    card_number     = db.Column(db.String(20), primary_key=True)
    renter_email    = db.Column(db.String(100), db.ForeignKey('renters.email', ondelete='CASCADE'), nullable=False)
    exp_date        = db.Column(db.Date)
    cvv             = db.Column(db.String(3))
    billing_address = db.Column(db.Integer, db.ForeignKey('addresses.address_id', ondelete='RESTRICT'), nullable=False)


class Property(db.Model):
    __tablename__ = 'properties'
    property_id    = db.Column(db.Integer, primary_key=True)
    agent_email    = db.Column(db.String(100), db.ForeignKey('agents.email', ondelete='CASCADE'), nullable=False)
    property_type  = db.Column(db.String(50), nullable=False)  # 'house','apartment','commercial'
    description     = db.Column(db.Text)
    street          = db.Column(db.String(255))
    city            = db.Column(db.String(100), nullable=False)
    state           = db.Column(db.String(50))
    price           = db.Column(db.Numeric(12,2), nullable=False)
    available_from  = db.Column(db.Date)
    available_to    = db.Column(db.Date)
    sqr_footage     = db.Column(db.Integer)

    house           = db.relationship('House', uselist=False, backref='property')
    apartment       = db.relationship('Apartment', uselist=False, backref='property')
    commercial      = db.relationship('CommercialBuilding', uselist=False, backref='property')
    bookings        = db.relationship('Booking', backref='property', cascade='all, delete-orphan')


class House(db.Model):
    __tablename__ = 'houses'
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id', ondelete='CASCADE'), primary_key=True)
    num_rooms   = db.Column(db.Integer)


class Apartment(db.Model):
    __tablename__ = 'apartments'
    property_id   = db.Column(db.Integer, db.ForeignKey('properties.property_id', ondelete='CASCADE'), primary_key=True)
    num_rooms     = db.Column(db.Integer)
    building_type = db.Column(db.String(100))


class CommercialBuilding(db.Model):
    __tablename__ = 'commercial_buildings'
    property_id   = db.Column(db.Integer, db.ForeignKey('properties.property_id', ondelete='CASCADE'), primary_key=True)
    business_type = db.Column(db.String(100))


class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id   = db.Column(db.Integer, primary_key=True)
    property_id  = db.Column(db.Integer, db.ForeignKey('properties.property_id', ondelete='CASCADE'), nullable=False)
    renter_email = db.Column(db.String(100), db.ForeignKey('renters.email', ondelete='CASCADE'), nullable=False)
    card_number  = db.Column(db.String(20), db.ForeignKey('credit_cards.card_number', ondelete='RESTRICT'), nullable=False)
    start_date   = db.Column(db.Date, nullable=False)
    end_date     = db.Column(db.Date, nullable=False)
    total_cost   = db.Column(db.Numeric(12,2), nullable=False)

