from flask import Flask, jsonify, request

app = Flask(__name__)

# ==========================================
# CƠ SỞ DỮ LIỆU (Database Mock)
# ==========================================
PRODUCTS_DB = [
    {"id": 1, "name": "Laptop Dell XPS", "price": 1200.0, "stock": 10},
    {"id": 2, "name": "iPhone 15 Pro", "price": 999.0, "stock": 50},
    {"id": 3, "name": "MacBook Air M2", "price": 1099.0, "stock": 20}
]

def get_all_products_from_db():
    """Giả lập hàm truy vấn CSDL chung cho tất cả các phiên bản API."""
    return PRODUCTS_DB

# ==========================================
# LỚP ADAPTER (Data Transfer Object - DTO)
# ==========================================
def adapter_v1(product):
    """
    Adapter V1: Ẩn các trường chi tiết (giá, tồn kho), chỉ trả về ID và Tên.
    """
    return {
        "id": product["id"],
        "name": product["name"]
    }

def adapter_v2(product):
    """
    Adapter V2: Trả về đầy đủ thông tin chi tiết và định dạng lại cấu trúc 
    (Ví dụ: đổi tên trường 'name' thành 'product_name').
    """
    return {
        "id": product["id"],
        "product_name": product["name"],
        "price_usd": product["price"],
        "is_available": product["stock"] > 0
    }

# ==========================================
# URL VERSIONING
# ==========================================
@app.route('/api/v1/products', methods=['GET'])
def get_products_v1():
    # 1. Gọi chung DB logic
    db_data = get_all_products_from_db()
    # 2. Map dữ liệu qua Adapter v1
    v1_data = [adapter_v1(p) for p in db_data]
    
    return jsonify({
        "version": "v1",
        "message": "Tra ve qua Adapter v1 (Co ban)",
        "data": v1_data
    }), 200

@app.route('/api/v2/products', methods=['GET'])
def get_products_v2():
    # 1. Gọi chung DB logic
    db_data = get_all_products_from_db()
    # 2. Map dữ liệu qua Adapter v2
    v2_data = [adapter_v2(p) for p in db_data]
    
    return jsonify({
        "version": "v2",
        "message": "Tra ve qua Adapter v2 (Chi tiet)",
        "data": v2_data
    }), 200

# ==========================================
# HEADER VERSIONING
# ==========================================
@app.route('/api/products', methods=['GET'])
def get_products_by_header():
    version = request.headers.get('Accept-Version', '1')
    db_data = get_all_products_from_db() # Dùng chung DB
    
    if version == '2':
        data = [adapter_v2(p) for p in db_data] # Adapter 2
        return jsonify({"version": "v2", "data": data}), 200
    else:
        data = [adapter_v1(p) for p in db_data] # Adapter 1
        return jsonify({"version": "v1", "data": data}), 200

# ==========================================
# USERS VERSIONING DEMO (v1 -> v2)
# ==========================================
USERS_DB = [
    {"id": 1, "first_name": "Nguyen", "last_name": "Van A", "age": 25},
    {"id": 2, "first_name": "Tran", "last_name": "Thi B", "age": 30}
]

@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    """
    API Users v1: Trả về fullname gộp chung.
    """
    data = [
        {
            "id": u["id"], 
            "fullname": f'{u["first_name"]} {u["last_name"]}', 
            "age": u["age"]
        } 
        for u in USERS_DB
    ]
    return jsonify({"version": "v1", "data": data}), 200

@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    """
    API Users v2: Trả về first_name và last_name tách biệt (Breaking Change từ v1).
    """
    return jsonify({"version": "v2", "data": USERS_DB}), 200


if __name__ == '__main__':
    print("=" * 50)
    print("[SERVER] Dang khoi chay Server Versioning Demo")
    print("\n--- PRODUCTS API ---")
    print("-> URL Versioning v1 : http://localhost:5000/api/v1/products")
    print("-> URL Versioning v2 : http://localhost:5000/api/v2/products")
    print("-> Header Versioning : http://localhost:5000/api/products (Can truyen Accept-Version: 1 hoac 2)")
    print("\n--- USERS API (Versioning v1 -> v2) ---")
    print("-> URL Versioning v1 : http://localhost:5000/api/v1/users (Tra ve fullname)")
    print("-> URL Versioning v2 : http://localhost:5000/api/v2/users (Tra ve first_name, last_name)")
    print("=" * 50)
    app.run(debug=True, port=5000)
