from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "available": True},
    {"id": 2, "title": "1984", "author": "George Orwell", "available": False}
]

loans = [
    {"id": 1, "book_id": 2, "user_id": 101, "status": "borrowed"}
]

@app.route('/api/books', methods=['GET'])
def get_books():
    """1. Lấy danh sách tài liệu/sách"""
    return jsonify(books), 200

@app.route('/api/books', methods=['POST'])
def add_book():
    """2. Thêm một sách mới vào thư viện"""
    data = request.json
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title"),
        "author": data.get("author"),
        "available": True
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """3. Xem thông tin chi tiết một cuốn sách"""
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """4. Cập nhật thông tin sách"""
    data = request.json
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        book["title"] = data.get("title", book["title"])
        book["author"] = data.get("author", book["author"])
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/loans', methods=['POST'])
def borrow_book():
    """5. Mượn sách (Tạo một loan record mới)"""
    data = request.json
    book_id = data.get("book_id")
    book = next((b for b in books if b["id"] == book_id), None)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if not book["available"]:
        return jsonify({"error": "Book is currently not available"}), 400
        
    book["available"] = False
    new_loan = {
        "id": len(loans) + 1,
        "book_id": book_id,
        "user_id": data.get("user_id"),
        "status": "borrowed"
    }
    loans.append(new_loan)
    return jsonify(new_loan), 201

if __name__ == '__main__':
    app.run(debug=True)