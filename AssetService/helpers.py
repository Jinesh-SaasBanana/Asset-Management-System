import requests
from functools import wraps
from flask import jsonify, request, g
from flask_jwt_extended import get_jwt, verify_jwt_in_request

# Replace this with your actual AuthService URL
AUTH_SERVICE_URL = "http://127.0.0.1:5000/auth"

def validate_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return None, "Authorization token is missing"

    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/validate",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code != 200:
            return None, "Invalid token"

        return response.json(), None  # Return jwt_data and None if valid

    except requests.exceptions.RequestException as e:
        return None, f"AuthService unreachable: {str(e)}"

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jwt_data, error = validate_token()
        
        if error:
            return jsonify({"error": error}), 401  # Return error response

        g.jwt_data = jwt_data  # Store the validated JWT data in g
        return fn(*args, **kwargs)

    wrapper.__name__ = fn.__name__
    return wrapper

def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in required_roles:
                return jsonify({"error": "You do not have access to this endpoint"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
