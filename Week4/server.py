from flask	 import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

books = [
	{
		"id": 1,
		"title": "Clean Code",
		"author": "Robert C. Martin",
		"genre": "Programming",
		"published_year": 2008,
		"price": 15.5,
		"is_available": True,
	},
	{
		"id": 2,
		"title": "The Pragmatic Programmer",
		"author": "Andrew Hunt",
		"genre": "Programming",
		"published_year": 1999,
		"price": 18.0,
		"is_available": True,
	},
	{
		"id": 3,
		"title": "Dune",
		"author": "Frank Herbert",
		"genre": "Sci-Fi",
		"published_year": 1965,
		"price": 12.3,
		"is_available": False,
	},
]


def _find_book(book_id: int):
	for b in books:
		if b["id"] == book_id:
			return b
	return None


@app.route("/api/v1/books", methods=["GET"])
def get_books():
	return jsonify(
		{
			"success": True,
			"data": books,
			"message": "Lấy danh sách sách thành công",
		}
	), 200


@app.route("/api/v1/books/search", methods=["GET"])
def search_books():
	# API truyền parameter qua query string: ?title=...
	title = request.args.get("title", "").strip().lower()
	result = [b for b in books if title in b["title"].lower()]

	return jsonify(
		{
			"success": True,
			"data": result,
			"message": "Tìm sách theo title thành công",
		}
	), 200


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
	book = _find_book(book_id)
	if not book:
		return jsonify({"success": False, "data": None, "message": "Không tìm thấy sách"}), 404

	return jsonify({"success": True, "data": book, "message": "Lấy sách thành công"}), 200


@app.route("/api/v1/books", methods=["POST"])
def create_book():
	data = request.get_json() or {}

	new_id = max([b["id"] for b in books], default=0) + 1
	new_book = {
		"id": new_id,
		"title": data.get("title", ""),
		"author": data.get("author", ""),
		"genre": data.get("genre", ""),
		"published_year": data.get("published_year", 0),
		"price": data.get("price", 0),
		"is_available": bool(data.get("is_available", True)),
	}

	books.append(new_book)
	return jsonify({"success": True, "data": new_book, "message": "Tạo sách thành công"}), 201


@app.route("/api/v1/books/<int:book_id>", methods=["PUT", "PATCH"])
def update_book(book_id):
	book = _find_book(book_id)
	if not book:
		return jsonify({"success": False, "data": None, "message": "Không tìm thấy sách"}), 404

	data = request.get_json() or {}

	book.update(data)

	return jsonify({"success": True, "data": book, "message": "Cập nhật sách thành công"}), 200


@app.route("/api/v1/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
	book = _find_book(book_id)
	if not book:
		return jsonify({"success": False, "data": None, "message": "Không tìm thấy sách"}), 404

	books.remove(book)
	return "", 204


if __name__ == "__main__":
	app.run(debug=True, port=5000)
