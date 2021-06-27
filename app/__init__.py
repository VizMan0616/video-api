from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from .common.config import Config

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)

    from .users.routes import users_bp
    from .videos.routes import videos_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(videos_bp)

    return app
