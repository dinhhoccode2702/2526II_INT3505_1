from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)

# Fake database (in-memory)
books = []
current_id = 1

# // add cors
CORS(app)


# GET /books - Get all books
@app.get("/books")
def get_books():
    return jsonify(books), 200


# POST /books - Create a new book
@app.post("/books")
def create_book():
    global current_id

    data = request.get_json()

    # Validate required fields
    if not data or "title" not in data or "author" not in data:
        abort(400, description="Missing required fields: title, author")

    new_book = {
        "id": current_id,
        "title": data["title"],
        "author": data["author"]
    }

    books.append(new_book)
    current_id += 1

    return jsonify(new_book), 201


# GET /books/{id} - Get book by ID
@app.get("/books/<int:id>")
def get_book(id):
    book = next((b for b in books if b["id"] == id), None)

    if not book:
        abort(404, description="Book not found")

    return jsonify(book), 200


# PUT /books/{id} - Update book
@app.put("/books/<int:id>")
def update_book(id):
    data = request.get_json()

    if not data or "title" not in data or "author" not in data:
        abort(400, description="Missing required fields: title, author")

    book = next((b for b in books if b["id"] == id), None)

    if not book:
        abort(404, description="Book not found")

    book["title"] = data["title"]
    book["author"] = data["author"]

    return jsonify(book), 200


# DELETE /books/{id} - Delete book
@app.delete("/books/<int:id>")
def delete_book(id):
    global books

    book = next((b for b in books if b["id"] == id), None)

    if not book:
        abort(404, description="Book not found")

    books = [b for b in books if b["id"] != id]

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)