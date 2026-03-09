from flask import Flask, jsonify, make_response, request
from functools import wraps

app = Flask(__name__)

# API key giả lập
API_KEYS = {
    "admin": "admin123",
    "user1": "user456"
}   

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"}
]

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        api_key = request.headers.get("API-Key")

        if not api_key:
            return jsonify({"error": "API-Key is missing"}), 401

        user = None
        for u, key in API_KEYS.items():
            if key == api_key:
                user = u

        if not user:
            return jsonify({"error": "Invalid API-Key"}), 401

        return f(user, *args, **kwargs)

    return decorated


@app.route("/products", methods=["GET"])
def get_products():
    response = make_response(jsonify(products))
    response.headers["Cache-Control"] = "public, max-age=60"
    return response


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for p in products:
        if p["id"] == id:
            return jsonify(p), 200

    return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["POST"])
@api_key_required
def create_product(current_user):

    data = request.json
    products.append(data)

    return jsonify({
        "data": data,
        "created_by": current_user
    }), 201


@app.route("/products/<int:id>", methods=["PUT"])
@api_key_required
def update_product(current_user, id):

    data = request.json

    for p in products:
        if p["id"] == id:
            p["name"] = data["name"]
            return jsonify({
                "data": p,
                "updated_by": current_user
            }), 200

    return jsonify({"error": "Product not found"}), 404


@app.route("/products/<int:id>", methods=["DELETE"])
@api_key_required
def delete_product(current_user, id):

    global products
    products = [p for p in products if p["id"] != id]

    return "", 204


    