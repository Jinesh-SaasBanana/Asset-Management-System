from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from AssetService.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)

    print('__init__.py')
    from AssetService.AssetServices import assets_bp
    print('__init__.py imported')
    app.register_blueprint(assets_bp, url_prefix="/assets")

    return app