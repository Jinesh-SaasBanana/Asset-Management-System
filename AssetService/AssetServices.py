print(__name__)
print(__name__ == "__main__")
from flask import jsonify, request, Blueprint, g
from AssetService.models import Asset
from AssetService import db, create_app
from AssetService.helpers import role_required, token_required

assets_bp = Blueprint("assets", __name__)

# Add a new asset
@assets_bp.route("/", methods=["POST"])
@token_required
@role_required(["Admin", "Assets Manager"])
def add_asset():
    data = request.json
    name = data.get("name")
    description = data.get("description", "")
    category = data.get("category")

    if not name or not category:
        return jsonify({"error": "Name and category are required"}), 400

    asset = Asset(name=name, description=description, category=category)
    db.session.add(asset)
    db.session.commit()

    return jsonify({"message": "Asset added successfully", "asset_id": asset.id}), 201

# Delete an asset
@assets_bp.route("/<int:asset_id>", methods=["DELETE"])
@token_required
@role_required(["Admin", "Assets Manager"])
def delete_asset(asset_id):
    asset = Asset.query.get(asset_id)

    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    db.session.delete(asset)
    db.session.commit()
    return jsonify({"message": f"Asset with ID {asset_id} has been deleted successfully"}), 200

# Assign an asset
@assets_bp.route("/assign/<int:asset_id>", methods=["PUT"])
@token_required
@role_required(["Admin", "HR"])
def assign_asset(asset_id):
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    if not asset.is_available:
        return jsonify({"error": "Asset is already assigned"}), 400

    asset.user_id = user_id
    asset.is_available = False
    db.session.commit()

    return jsonify({"message": f"Asset {asset_id} assigned to user {user_id}"}), 200

# Release an asset
@assets_bp.route("/release/<int:asset_id>", methods=["PUT"])
@token_required
@role_required(["Admin", "Employee"])
def release_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    claims = g.jwt_data
    user = claims["user"]

    if asset.user_id != user or claims["role"] != "Admin":
        print(asset.user_id != user, claims["role"] != "Admin")
        print(asset.user_id, user, claims["role"])
        return jsonify({"error": "You are not authorized to release this asset"}), 403

    asset.user_id = None
    asset.is_available = True
    db.session.commit()

    return jsonify({"message": f"Asset {asset_id} released"}), 200

# Get all assets
@assets_bp.route("/", methods=["GET"])
@token_required
@role_required(["Admin", "Assets Manager", "HR", "Employee"])
def get_assets():
    user_id = request.args.get("user_id")
    is_available = request.args.get("is_available")

    query = Asset.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if is_available is not None:
        query = query.filter_by(is_available=is_available.lower() == "true")

    assets = query.all()
    return jsonify([
        {
            "id": asset.id,
            "name": asset.name,
            "description": asset.description,
            "category": asset.category,
            "is_available": asset.is_available,
            "user_id": asset.user_id
        } for asset in assets
    ]), 200

app = create_app()
if __name__ == "__main__":
    pass
    # app.run(port=8000, debug=True)