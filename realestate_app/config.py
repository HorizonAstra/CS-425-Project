import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://realestate_user:StrongPass!@localhost/realestate_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
