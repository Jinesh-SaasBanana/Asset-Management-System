from marshmallow import fields, validate, ValidationError
from AssetService import db, ma

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, nullable=True)

class AssetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset
        load_instance = True

    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=255))
    category = fields.String(required=True, validate=validate.Length(min=1, max=50))
    is_available = fields.Boolean(dump_only=True)
    user_id = fields.Integer(
        allow_none=True,
        validate=lambda x: x is None or x > 0,
        error_messages={"validator_failed": "User ID must be a positive integer or null."}
    )