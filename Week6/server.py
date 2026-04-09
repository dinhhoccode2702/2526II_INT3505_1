from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY_KTHDV'

# ==========================================
# GIẢ LẬP DATABASE
# ==========================================
users_db = [
    {"id": 1, "username": "sinhvien", "password": "123", "role": "USER",  "name": "Nguyễn Văn A"},
    {"id": 2, "username": "giangvien", "password": "456", "role": "ADMIN", "name": "Tiến sĩ Đoàn B"}
]

def get_user_by_id(user_id):
    return next((u for u in users_db if u["id"] == user_id), None)

def get_user_by_username(username):
    return next((u for u in users_db if u["username"] == username), None)

# ==========================================
# KHỞI TẠO CẶP TOKEN (Access + Refresh)
# Gọi 1 hàm này là đẻ ra cả 2 loại thẻ
# ==========================================
def create_tokens(user_id, role, scopes=[]):
    access_token = jwt.encode({
        'user_id': user_id,
        'role': role,
        'scopes': scopes,              # Danh sách quyền được cấp
        'token_type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    refresh_token = jwt.encode({
        'user_id': user_id,
        'token_type': 'refresh',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return access_token, refresh_token

# ==========================================
# DECORATOR 1: Kiểm tra Access Token
# Dán @token_required trước route muốn bảo vệ
# ==========================================
def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = None

        # Cách 1: Lấy token từ Header (Phương thức thông thường)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if "Bearer" in auth_header:
                token = auth_header.split()[1]

        # Cách 2: Lấy token từ HttpOnly Cookie (Phương thức bảo mật - JS không sờ được)
        if not token:
            token = request.cookies.get('access_token')

        if not token:
            return jsonify({'error': 'Yêu cầu Access Token hợp lệ!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            if data.get('token_type') != 'access':
                return jsonify({'error': 'Sai loại Token! Chỉ chấp nhận Access Token.'}), 401
            request.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Access Token hết hạn! Dùng Refresh Token để đổi vé mới.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token không hợp lệ!'}), 401

        return f(*args, **kwargs)
    return check_token

# ==========================================
# DECORATOR 2: Kiểm tra Role (Phân quyền)
# Dán @role_required('ADMIN') sau @token_required
# ==========================================
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def check_role(*args, **kwargs):
            user_data = getattr(request, 'current_user', None)

            if not user_data or user_data.get('role') != required_role:
                return jsonify({
                    'error': 'Từ chối truy cập! Bạn không đủ thẩm quyền.',
                    'required_role': required_role,
                    'your_role': user_data.get('role') if user_data else None
                }), 403

            return f(*args, **kwargs)
        return check_role
    return decorator

# ==========================================
# DECORATOR 3: Kiểm tra Scope (Phạm vi quyền)
# Dán @scope_required('write:transfer') để bảo vệ hành động nhạy cảm
# ==========================================
def scope_required(required_scope):
    def decorator(f):
        @wraps(f)
        def check_scope(*args, **kwargs):
            user_data = getattr(request, 'current_user', None)
            granted_scopes = user_data.get('scopes', []) if user_data else []

            if required_scope not in granted_scopes:
                return jsonify({
                    'error': 'Không đủ phạm vi quyền hạn (Scope) để thực hiện hành động này!',
                    'required_scope': required_scope,
                    'your_scopes': granted_scopes
                }), 403

            return f(*args, **kwargs)
        return check_scope
    return decorator

# ==========================================
# CÁC ROUTE API
# ==========================================

# API 1: Đăng nhập
# Client khai báo muốn xin những quyền (scopes) gì
# Ví dụ gửi: { "username": "sinhvien", "password": "123", "scopes": ["read:profile"] }
# Nếu không gửi scopes → chỉ có quyền cơ bản, KHÔNG có quyền chuyển tiền
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = get_user_by_username(data.get('username'))

    # Lấy danh sách quyền mà client XIN (Giống bạn bấm "Cho phép" trên popup OAuth)
    requested_scopes = data.get('scopes', [])  # Mặc định: không xin quyền gì thêm

    if user and user['password'] == data.get('password'):
        access, refresh = create_tokens(user['id'], user['role'], requested_scopes)
        return jsonify({
            "message": "Đăng nhập thành công!",
            "access_token": access,
            "refresh_token": refresh,
            "granted_scopes": requested_scopes,  # Cho thấy đã cấp những quyền nào
            "user_info": {"name": user['name'], "role": user['role']}
        }), 200

    return jsonify({"error": "Tài khoản hoặc mật khẩu không chính xác."}), 401

# API 2: Đổi thẻ - Nhận Refresh Token cũ, trả về cặp Token mới (Rotation)
@app.route('/api/refresh', methods=['POST'])
def refresh():
    r_token = request.json.get('refresh_token')

    if not r_token:
        return jsonify({'error': 'Cung cấp Refresh Token để tiếp tục!'}), 400

    try:
        payload = jwt.decode(r_token, app.config['SECRET_KEY'], algorithms=["HS256"])

        # Chặn việc dùng Access Token đến cổng này để đổi thẻ
        if payload.get('token_type') != 'refresh':
            return jsonify({'error': 'Đây không phải Refresh Token!'}), 401

        user = get_user_by_id(payload['user_id'])
        if not user:
            return jsonify({'error': 'Người dùng không tồn tại!'}), 404

        new_access, new_refresh = create_tokens(user['id'], user['role'])
        return jsonify({
            "message": "Cấp lại Token thành công!",
            "access_token": new_access,
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh Token hết hạn! Vui lòng đăng nhập lại.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Refresh Token không hợp lệ!'}), 401

# API 3: Tin tức công khai - Không cần Token
@app.route('/public/news', methods=['GET'])
def get_public_news():
    return jsonify({"news": "Thông báo: Thay đổi lịch đào tạo tuần tới."}), 200

# API 4: Xem hồ sơ - Cần Access Token (Authentication)
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    user_data = request.current_user
    return jsonify({
        "message": "Trích xuất hồ sơ cá nhân thành công.",
        "user_id": user_data['user_id'],
        "role": user_data['role']
    }), 200

# API 5: Dashboard Admin - Cần Access Token VÀ phải là ADMIN (Authorization)
@app.route('/api/admin/dashboard', methods=['GET'])
@token_required
@role_required('ADMIN')
def get_dashboard():
    return jsonify({
        "message": "Dữ liệu giám sát hệ thống.",
        "cpu_usage": "45%",
        "status": "Secure"
    }), 200

# API 6: Chuyển tiền - Cần Token VÀ phải có Scope 'write:transfer'
# Demo: Scope kiểm soát HÀNH ĐỘNG CỤ THỂ, không phải vai trò con người
@app.route('/api/transfer', methods=['POST'])
@token_required
@scope_required('write:transfer')  # Chỉ cho phép nếu Token có ghi scope này
def transfer_money():
    amount = request.json.get('amount', 0)
    return jsonify({"message": f"Khởi tạo giao dịch {amount} VNĐ thành công."}), 200


# =====================================================================
# DEMO CHỐNG XSS: Đăng nhập an toàn bằng HttpOnly Cookie
# =====================================================================

# API 7: Đăng nhập bảo mật (Lưu Token vào HttpOnly Cookie)
# So sánh với API /login thông thường trả token trong JSON Body
@app.route('/api/login-secure', methods=['POST'])
def login_secure():
    data = request.json
    user = get_user_by_username(data.get('username'))

    if user and user['password'] == data.get('password'):
        access, refresh = create_tokens(user['id'], user['role'])

        # Thay vì trả token trong JSON → Nét thẳng vào Cookie
        response = make_response(jsonify({
            "message": "Đăng nhập an toàn thành công!",
            "note": "Token được lưu trong HttpOnly Cookie. JavaScript không thể đọc được!",
            "user_info": {"name": user['name'], "role": user['role']}
        }))

        response.set_cookie(
            'access_token',
            access,
            httponly=True,    
            secure=False,     
            samesite='Lax',
            max_age=15 * 60   
        )
        return response, 200

    return jsonify({"error": "Tài khoản hoặc mật khẩu không chính xác."}), 401


# API 8: Đăng xuất - Xóa Cookie
@app.route('/api/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "Đăng xuất thành công. Cookie đã bị xóa."}))
    response.delete_cookie('access_token')
    return response, 200


if __name__ == '__main__':
    print("Starting API server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
