from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập Database (Mock Data)
PRODUCTS_DB = [
    {"id": 1, "name": "Laptop Dell XPS", "price": 1200.0},
    {"id": 2, "name": "iPhone 15 Pro", "price": 999.0},
    {"id": 3, "name": "MacBook Air M2", "price": 1099.0}
]

# ==========================================
# VERSION 1: API Trả về thông tin cơ bản (Tên)
# ==========================================
@app.route('/api/v1/products', methods=['GET'])
def get_products_v1():
    """
    API v1: Chỉ trả về danh sách các sản phẩm với ID và Tên.
    """
    v1_data = [{"id": p["id"], "name": p["name"]} for p in PRODUCTS_DB]
    
    return jsonify({
        "version": "v1",
        "message": "Lấy danh sách sản phẩm thành công",
        "data": v1_data
    }), 200


# ==========================================
# VERSION 2: API Trả về thông tin chi tiết (Tên + Giá)
# ==========================================
@app.route('/api/v2/products', methods=['GET'])
def get_products_v2():
    """
    API v2: Cung cấp đầy đủ thông tin sản phẩm bao gồm cả Giá (price).
    """
    return jsonify({
        "version": "v2",
        "message": "Lấy danh sách sản phẩm thành công (bản chi tiết)",
        "data": PRODUCTS_DB
    }), 200


# ==========================================
# HEADER VERSIONING: Chung URL, định tuyến theo Header
# ==========================================
@app.route('/api/products', methods=['GET'])
def get_products_by_header():
    """
    Header Versioning: Đọc header 'Accept-Version' để quyết định format response.
    Mặc định (nếu không truyền) sẽ trả về v1.
    """
    version = request.headers.get('Accept-Version', '1')
    
    if version == '2':
        return jsonify({
            "version": "v2",
            "message": "Da nhan Header Version 2 (Chi tiet)",
            "data": PRODUCTS_DB
        }), 200
    else:
        v1_data = [{"id": p["id"], "name": p["name"]} for p in PRODUCTS_DB]
        return jsonify({
            "version": "v1",
            "message": "Da nhan Header Version 1 hoac mac dinh (Co ban)",
            "data": v1_data
        }), 200


if __name__ == '__main__':
    print("=" * 50)
    print("[SERVER] Dang khoi chay Server Versioning Demo")
    print("-> URL Versioning v1 : http://localhost:5000/api/v1/products")
    print("-> URL Versioning v2 : http://localhost:5000/api/v2/products")
    print("-> Header Versioning : http://localhost:5000/api/products (Can truyen Accept-Version: 1 hoac 2)")
    print("=" * 50)
    app.run(debug=True, port=5000)
