from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from AuthService.config import Config

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from AuthService.AuthServices import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
