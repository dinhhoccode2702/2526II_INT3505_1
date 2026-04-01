from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
# Khóa bí mật dùng để mã hóa và giải mã JWT
app.config['SECRET_KEY'] = 'SECRET_KEY_KTHDV'

# ==========================================
# GIẢ LẬP DATABASE (Lưu trên RAM)
# Chuyển thành dạng mảng (List) để giống cấu trúc bảng Record dưới DB
# ==========================================
users_db = [
    {
        "id": 1,
        "username": "sinhvien",
        "password": "123", # User 1: Dành để test quyền USER
        "role": "USER",
        "name": "Nguyễn Văn A"
    },
    {
        "id": 2,
        "username": "giangvien",
        "password": "456", # User 2: Dành để test quyền ADMIN
        "role": "ADMIN",
        "name": "Tiến sĩ Đoàn B"
    }
]

# Hàm rút trích user từ Database giả lập
def get_user_by_username(username):
    # Trả về User đầu tiên khớp Tên đăng nhập
    return next((u for u in users_db if u["username"] == username), None)

# ==========================================
# MIDDLEWARE KIỂM TRA TOKEN (JWT)
# ==========================================
def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = None
        # Lấy token từ Header "Authorization: Bearer <token>"
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if "Bearer" in auth_header:
                token = auth_header.split()[1] 

        if not token:
            return jsonify({'error': 'Không tìm thấy Token xác thực!'}), 401
        
        try:
            # Giải mã Token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Lưu payload vào request để sử dụng ở các hàm API phía sau
            request.current_user = data 
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token đã hết hạn!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token không hợp lệ!'}), 401
        
        return f(*args, **kwargs) 
    return check_token

# ==========================================
# MIDDLEWARE PHÂN QUYỀN (AUTHORIZATION)
# ==========================================
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def check_role(*args, **kwargs):
            # Biến này đã được sinh ra từ Middleware `token_required` ở trên chạy trước
            user_data = getattr(request, 'current_user', None)
            
            # Cơ chế vặn quyền (Check Role) - Trả về Lỗi 403 Forbidden nếu không đủ cấp
            if not user_data or user_data.get('role') != required_role:
                return jsonify({
                    'error': 'Từ chối truy cập (Forbidden). Bạn không đủ thẩm quyền!',
                    'required_role': required_role,
                    'current_role': user_data.get('role') if user_data else None
                }), 403
            
            return f(*args, **kwargs)
        return check_role
    return decorator

# ==========================================
# CÁC ROUTE API
# ==========================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Tra cứu User từ DB
    user = get_user_by_username(username)

    if user and user['password'] == password:
        # Bước 1: Khởi tạo Token (Lưu ID và Chức vụ, TTL: 15 phút)
        token = jwt.encode({
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "message": f"Đăng nhập thành công!", 
            "access_token": token,
            "user_info": {"name": user['name'], "role": user['role']}
        }), 200
    
    return jsonify({"error": "Tài khoản hoặc mật khẩu không chính xác."}), 401

@app.route('/public/news', methods=['GET'])
def get_public_news():
    return jsonify({"news": "Thông báo: Thay đổi lịch đào tạo tuần tới."}), 200

@app.route('/api/profile', methods=['GET'])
@token_required # Bắt buộc phải có thẻ JWT hợp lệ để chạy hàm này
def get_profile():
    # Lấy thông tin user gửi lên từ Middleware `token_required`
    user_data = request.current_user 
    return jsonify({
        "message": "Trích xuất hồ sơ cá nhân thành công.", 
        "gpa": "3.8",
        "token_payload": user_data 
    }), 200

@app.route('/api/admin/dashboard', methods=['GET'])
@token_required          
@role_required('ADMIN') 
def get_dashboard():
    return jsonify({"message": "Lấy dữ liệu giám sát hệ thống thành công.", "cpu_usage": "45%"}), 200

@app.route('/api/transfer', methods=['POST'])
def transfer_money():
    data = request.json
    amount = data.get('amount', 0)
    return jsonify({"message": f"Khởi tạo giao dịch chuyển khoản {amount} VNĐ thành công."}), 200

if __name__ == '__main__':
    print("Khởi động Máy chủ API tại http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
