from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from AuthService.models import User
from AuthService import db, create_app

auth_bp = Blueprint("auth", __name__)

# Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")  # Admin, Assets Manager, HR, Employee

    if not username or not password or not role:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Login user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401
    identity = str(user.id)
    additional_claims = {"username": user.username, "role": user.role}

    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    jwt_data = get_jwt()
    username = jwt_data["username"]
    role = jwt_data["role"]

    return jsonify({"message": f"Hello {username}, your role is {role}."}), 200
app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)