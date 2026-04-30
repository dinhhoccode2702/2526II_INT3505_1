from flask import Flask, jsonify, request, make_response
from functools import wraps
import logging
import datetime

app = Flask(__name__)

# Cấu hình logging để in cảnh báo ra console của Backend
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# ==========================================
# DECORATOR: CẢNH BÁO DEVELOPER TỰ ĐỘNG
# ==========================================
def notify_deprecation(sunset_date, replacement_url):
    """
    Decorator này được gắn vào các hàm API cũ.
    Nhiệm vụ:
    1. Ghi log cảnh báo trên Backend (để biết ai đang gọi).
    2. Chèn HTTP Headers chuẩn (Deprecation, Sunset, Link) vào Response gửi về Client.
    3. Chèn thêm Header Warning (HTTP Warning Header) để phần mềm Client báo lỗi.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Cảnh báo trên Server Log (giúp DevOps theo dõi)
            client_ip = request.remote_addr
            logging.warning(f"[DEPRECATION ALERT] Endpoint '{request.path}' is deprecated! Called by IP: {client_ip}")
            
            # Thực thi hàm API gốc
            response_data = f(*args, **kwargs)
            
            # Convert dict sang Flask Response object nếu cần
            if not isinstance(response_data, app.response_class):
                if isinstance(response_data, tuple): # Xử lý trường hợp return jsonify(), 200
                    response = make_response(response_data[0])
                    response.status_code = response_data[1]
                else:
                    response = make_response(response_data)
            else:
                response = response_data
            
            # 2. Inject Headers thông báo cho Developer đang code ở Client
            response.headers['Deprecation'] = 'true'
            response.headers['Sunset'] = sunset_date
            response.headers['Link'] = f'<{replacement_url}>; rel="alternate"'
            
            # Header Warning tiêu chuẩn HTTP
            response.headers['Warning'] = f'299 - "Deprecated API: Endpoint này sẽ bị tắt vào {sunset_date}. Vui lòng chuyển sang dùng {replacement_url}"'
            
            return response
        return decorated_function
    return decorator

# ==========================================
# ENDPOINTS DEMO
# ==========================================

# Gắn Decorator vào API cũ để tự động thông báo
@app.route('/api/v1/orders', methods=['GET'])
@notify_deprecation(sunset_date="Fri, 01 Jan 2027 23:59:59 GMT", replacement_url="/api/v2/orders")
def get_orders_v1():
    # Giả lập payload gốc
    data = [
        {"order_id": 101, "total": 500},
        {"order_id": 102, "total": 300}
    ]
    
    # TÙY CHỌN: Chèn thêm cảnh báo trực tiếp vào JSON body để Developer thấy ngay lập tức
    payload = {
        "_developer_warning": "BẢN V1 NÀY SẮP BỊ XÓA. HÃY CẬP NHẬT LÊN V2 NHÉ!",
        "data": data
    }
    
    return jsonify(payload), 200


@app.route('/api/v2/orders', methods=['GET'])
def get_orders_v2():
    data = [
        {"id": 101, "total_amount": 500},
        {"id": 102, "total_amount": 300}
    ]
    return jsonify({"data": data, "version": "v2"}), 200

if __name__ == '__main__':
    print("="*60)
    print("🚀 Khởi chạy Server Demo: Developer Deprecation Notification")
    print("="*60)
    print("Hãy mở Postman và gọi GET: http://127.0.0.1:5000/api/v1/orders")
    print("1. Chú ý màn hình Console này (sẽ in log cảnh báo đỏ).")
    print("2. Chú ý tab Headers trong Postman (sẽ thấy Warning, Deprecation).")
    print("3. Chú ý JSON Body trả về (sẽ thấy field _developer_warning).")
    print("="*60)
    app.run(debug=True, port=5000)
