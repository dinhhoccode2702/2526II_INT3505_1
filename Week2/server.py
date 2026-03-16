import datetime

from flask import Flask, jsonify, make_response, request 
import jwt
from functools import wraps

app = Flask(__name__)

SECRET_KEY = "mysecretkey"

user = [ {
            "username": "ndinh",
            "password": "123456"
         }
]

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"}
]

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        token = auth_header.split(" ")[1]

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = data["user"]
      
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(user, *args, **kwargs)

    return decorated

# login to get token
@app.route("/login", methods=["POST"])
def login():

    data = request.json
    username = data.get("username")
    password = data.get("password")

    for u in user:
        if u["username"] == username and u["password"] == password:
            token = jwt.encode(
                {
                    "user": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },
                SECRET_KEY,
                algorithm="HS256",
                headers={"alg": "HS256", "typ": "JWT"}
            )

            return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/products", methods=["GET"])
def get_products():
    response = make_response(jsonify(10/0), 200)
    response.headers["Cache-Control"] = "public, max-age=60"
    return response


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for p in products:
        if p["id"] == id:
            return jsonify(p), 200

    return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["POST"])
@jwt_required
def create_product(current_user):

    data = request.json
    products.append(data)

    return jsonify({
        "data": data,
        "created_by": current_user
    }), 201


@app.route("/products/<int:id>", methods=["PUT"])
@jwt_required
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
@jwt_required
def delete_product(current_user, id):

    global products
    products = [p for p in products if p["id"] != id]

    return "", 204

if __name__ == "__main__":
    app.run(debug=True)