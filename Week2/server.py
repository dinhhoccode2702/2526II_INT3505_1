from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"}
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for p in products:
        if p["id"] == id:
            return jsonify(p), 200

    return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    products.append(data)

    return jsonify(data), 201

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.json
    for p in products:
        if p["id"] == id:
            p["name"] = data["name"]
            return jsonify(p)
    return jsonify({"error": "Product not found"}), 404

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    global products
    products = [p for p in products if p["id"] != id]

    return "", 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)