from AuthService import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError, validates

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Admin, Assets Manager, HR, Employee

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
    password_hash = ma.auto_field(dump_only=True)
    role = ma.String(validate=lambda r: r in ["Admin", "Assets Manager", "HR", "Employee"])
    username = ma.String(required=True, validate=lambda u: len(u) >= 3, error_messages={"required": "Username is required."})

    @validates("username")
    def validate_username(self, value):
        if not value.isalnum():
            raise ValidationError("Username must contain only alphanumeric characters.")
        if len(value) > 30:
            raise ValidationError("Username must be less than or equal to 30 characters.")
        
    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/`~" for char in value):
            raise ValidationError("Password must contain at least one special character.")