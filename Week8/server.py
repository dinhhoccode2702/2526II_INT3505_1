from flask import Flask, request, jsonify
import time
import math
from mongoengine import connect

app = Flask(__name__)
connect(host="mongodb://localhost:27017/test")
print("[OK] Da ket noi MongoDB thanh cong!")


# Mock Database
users_db = {
    1: {"id": 1, "name": "Nguyen Van A", "email": "nva@gmail.com"},
    2: {"id": 2, "name": "Tran Thi B", "email": "ttb@gmail.com"},
    3: {"id": 3, "name": "Le Van C", "email": "lvc@gmail.com"}
}
current_user_id = 4

# 1. Simple GET - Dùng cho Unit Test cơ bản
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    }), 200

# 2. POST với validate đầu vào - Dùng cho Unit/Integration Test (Kiểm tra validate, trạng thái DB)
@app.route('/api/users', methods=['POST'])
def create_user():
    global current_user_id
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Thiếu thông tin name hoặc email"}), 400
        
    user = {
        "id": current_user_id,
        "name": data['name'],
        "email": data['email']
    }
    users_db[current_user_id] = user
    current_user_id += 1
    
    return jsonify(user), 201

# 3. GET với tham số trên URL (Path Parameter) - Dùng cho Unit/Integration Test
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Không tìm thấy user"}), 404

# 4. POST với Logic nghiệp vụ
@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({"error": "Không có items trong giỏ"}), 400
        
    total = 0
    for item in data['items']:
        if 'price' not in item or 'quantity' not in item:
            return jsonify({"error": "Sai định dạng item"}), 400
        total += item['price'] * item['quantity']
        
    if total > 5000:
        return jsonify({"error": "Vượt quá hạn mức thanh toán"}), 403
        
    return jsonify({
        "status": "success", 
        "total_paid": total, 
        "receipt": "REC-" + str(int(time.time()))
    }), 200

# 5. Tác vụ nặng về CPU - Dùng cho Performance/Load Test
@app.route('/api/heavy-calculation', methods=['GET'])
def heavy_calculation():
    # Lấy tham số, mặc định là tính toán với O(n^2)
    n = request.args.get('n', default=1000, type=int)
    if n > 50000:
        n = 50000 # Chặn n quá lớn tránh crash server
        
    # Mô phỏng tác vụ nặng tìm số nguyên tố
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            
    return jsonify({
        "status": "completed",
        "items_found": len(primes)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
