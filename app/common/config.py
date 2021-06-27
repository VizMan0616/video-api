import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('FLASK_DATABASE')
    JSON_SORT_KEYS = False
