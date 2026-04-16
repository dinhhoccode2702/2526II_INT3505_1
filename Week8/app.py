from flask import Flask, request, jsonify
from mongoengine import connect, Document, StringField, IntField, errors
import math
import time

app = Flask(__name__)

# 1. Khai báo Schema cho MongoDB
class User(Document):
    user_id = IntField(required=True, unique=True)
    name = StringField(required=True)
    email = StringField(required=True)
    meta = {'collection': 'users'}

# 2. Kết nối Database (Dùng chữ 'Test' hoa để tránh lỗi trên Windows của bạn)
try:
    connect(db="Test", host="mongodb://localhost:27017/Test")
    print("[OK] Đã kết nối MongoDB thành công!")
except Exception as e:
    print(f"[Error] Lỗi kết nối DB: {e}")

# 3. ENDPOINTS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    }), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Thiếu thông tin name hoặc email"}), 400
    
    try:
        # Lấy timestamp làm ID đơn giản hoặc dùng ID từ data nếu có
        u_id = data.get('user_id', int(time.time() * 1000) % 1000000)
        
        new_user = User(
            user_id=u_id,
            name=data['name'],
            email=data['email']
        ).save()
        
        return jsonify({
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email
        }), 201
    except errors.NotUniqueError:
        return jsonify({"error": "ID người dùng đã tồn tại"}), 409

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Tìm user trong MongoDB thay vì dùng dict
    user = User.objects(user_id=user_id).first()
    if user:
        return jsonify({
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email
        }), 200
    return jsonify({"error": "Không tìm thấy user"}), 404

# --- ENDPOINT 4: Thanh toán giỏ hàng ---
@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    items = data.get('items', [])
    
    # Tính tổng tiền: sum(price * quantity)
    total_amount = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    
    # Logic nghiệp vụ: Hạn mức 5000
    if total_amount > 5000:
        return jsonify({
            "status": "error",
            "message": f"Vượt quá hạn mức thanh toán (Total: {total_amount})"
        }), 403 # Forbidden
    
    return jsonify({
        "status": "success",
        "total_paid": total_amount
    }), 200

# --- ENDPOINT 5: Tính toán nặng (Giả lập hiệu năng) ---
@app.route('/api/heavy-calculation', methods=['GET'])
def heavy_calc():
    n = int(request.args.get('n', 1000))
    start_time = time.time()
    
    # Giả lập một vòng lặp tốn tài nguyên
    result = sum(i * i for i in range(n))
    
    end_time = time.time()
    return jsonify({
        "result": result,
        "execution_time_ms": (end_time - start_time) * 1000
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)