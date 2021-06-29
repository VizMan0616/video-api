import os
from datetime import timedelta as td


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DATABASE')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JSON_SORT_KEYS = False

