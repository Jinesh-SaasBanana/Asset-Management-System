from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from AssetService.config import Config

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)

    from AssetService.AssetServices import assets_bp
    app.register_blueprint(assets_bp, url_prefix="/assets")

    return app
