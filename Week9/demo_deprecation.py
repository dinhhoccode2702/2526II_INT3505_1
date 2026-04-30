from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Giả lập Database đơn giản
MOCK_DB = {
    1: {"id": 1, "first_name": "Nguyen", "last_name": "Van A", "age": 25},
    2: {"id": 2, "first_name": "Tran", "last_name": "Thi B", "age": 30}
}

# ---------------------------------------------------------
# API v1 (Sắp bị khai tử - Deprecated)
# ---------------------------------------------------------
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user_v1(user_id):
    user = MOCK_DB.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Ở v1, dữ liệu trả về gộp first_name và last_name thành fullname
    # Giả sử giờ ta muốn đổi cấu trúc (tách first, last), đó là 1 Breaking change.
    data_v1 = {
        "user_id": user["id"],
        "fullname": f'{user["first_name"]} {user["last_name"]}',
        "age": user["age"],
        # Có thể nhúng thêm field warning (tùy chọn) để frontend in ra console
        "_warning": "This endpoint is deprecated and will be removed on Jan 1st, 2027. Please migrate to /api/v2/users"
    }

    response = make_response(jsonify(data_v1))
    
    # Thêm các HTTP Headers theo tiêu chuẩn cho Deprecation
    # Deprecation: Ngày bắt đầu cảnh báo
    response.headers['Deprecation'] = 'Fri, 01 May 2026 23:59:59 GMT'
    # Sunset: Ngày chính thức "rút phích cắm" (tắt API)
    response.headers['Sunset'] = 'Fri, 01 Jan 2027 23:59:59 GMT'
    # Link: Trỏ tới Endpoint thay thế
    response.headers['Link'] = f'</api/v2/users/{user_id}>; rel="alternate"'

    return response

# ---------------------------------------------------------
# API v2 (API Mới - Khuyên dùng)
# ---------------------------------------------------------
@app.route('/api/v2/users/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):
    user = MOCK_DB.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Ở v2, cấu trúc đã chuẩn hóa hơn
    data_v2 = {
        "id": str(user["id"]), # Chuyển id thành chuỗi (Giả lập breaking change)
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "age": user["age"]
    }

    return jsonify(data_v2)

# ---------------------------------------------------------
# API v0 (Ví dụ API đã khai tử hoàn toàn - Sunset)
# ---------------------------------------------------------
@app.route('/api/v0/users/<int:user_id>', methods=['GET'])
def get_user_v0(user_id):
    # Dùng status code 410 (Gone) thay vì 404 (Not Found)
    # Để báo cho client biết rằng URL này từng tồn tại nhưng đã bị xóa vĩnh viễn
    return jsonify({
        "error": "Gone",
        "message": "This API version (v0) was permanently removed on Jan 1st, 2025. Please use v2."
    }), 410

if __name__ == '__main__':
    print("🚀 Server is running on http://127.0.0.1:5000")
    print("Try the following endpoints in Postman:")
    print("1. GET http://127.0.0.1:5000/api/v1/users/1 (Deprecated)")
    print("2. GET http://127.0.0.1:5000/api/v2/users/1 (New)")
    print("3. GET http://127.0.0.1:5000/api/v0/users/1 (Sunset / Removed)")
    app.run(debug=True, port=5000)
