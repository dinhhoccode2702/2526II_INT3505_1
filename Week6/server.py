from flask import Flask, request, jsonify

app = Flask(__name__)

# Giả lập Cơ sở dữ liệu (In-memory Database)
# Chú ý: Ở bài thực tế, mật khẩu phải được băm (bcrypt) trước khi lưu
users_db = {
    "sinhvien1": {
        "id": 1,
        "password": "123", 
        "role": "USER",
        "name": "Nguyễn Văn Sinh Viên"
    },
    "thaygiao": {
        "id": 2,
        "password": "456",
        "role": "ADMIN",
        "name": "Tiến sĩ A"
    }
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)
    if user and user['password'] == password:
        return jsonify({
            "message": f"Xin chào {user['name']}", 
            "status": "Chưa có Token, lát mình code vô đoạn này!"
        }), 200
    
    return jsonify({"error": "Đăng nhập thất bại. Chắc nhìn nhầm pass!"}), 401

@app.route('/public/news', methods=['GET'])
def get_public_news():
    return jsonify({"news": "Sáng mai trường cho nghỉ học do cúp điện"}), 200

@app.route('/api/profile', methods=['GET'])
def get_profile():
    # Tạm thời chưa bảo mật, mở cửa thả cửa
    return jsonify({"message": "Đây là hồ sơ mật của bạn", "gpa": "3.8"}), 200

@app.route('/api/admin/dashboard', methods=['GET'])
def get_dashboard():
    return jsonify({"secret_logs": "Hệ thống đang bị quá tải, sếp tăng lương đi!"}), 200

@app.route('/api/transfer', methods=['POST'])
def transfer_money():
    data = request.json
    amount = data.get('amount', 0)
    return jsonify({"message": f"Biến động số dư: Trừ {amount}$ đi vào hư vô"}), 200


if __name__ == '__main__':
    print("🔥 Khởi động Server thành công! API lắng nghe ở Cổng 5000...")
    app.run(debug=True, port=5000)
