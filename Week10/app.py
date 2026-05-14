from flask import Flask, jsonify, request
from logger_config import logger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from circuitbreaker import circuit, CircuitBreakerError
import traceback
import time
import random

app = Flask(__name__)

# Setup Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per 15 minutes"],
    storage_uri="memory://",
)

# Global flag to simulate 3rd party API status
PAYMENT_GATEWAY_UP = True

# --- Circuit Breaker Logic ---
# Cấu hình: failure_threshold=5 (lỗi 5 lần liên tiếp sẽ ngắt mạch)
# recovery_timeout=30 (sau 30s sẽ thử lại - Half-Open)
@circuit(failure_threshold=5, recovery_timeout=30)
def call_external_payment_gateway():
    if not PAYMENT_GATEWAY_UP:
        # Giả lập timeout hoặc lỗi kết nối
        time.sleep(2)  # Giả lập chờ đợi
        raise Exception("Payment Gateway is Down (Timeout Simulation)")
    
    # Giả lập thành công
    return {"status": "success", "transaction_id": random.randint(1000, 9999)}

# Mock data
users = [
    {"id": 1, "username": "admin", "role": "admin"},
    {"id": 2, "username": "devops_engineer", "role": "user"}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    logger.info("Fetching all users", extra={"path": request.path, "method": request.method})
    return jsonify(users), 200

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
        
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Login attempt missing credentials", extra={
            "path": request.path,
            "ip": request.remote_addr
        })
        return jsonify({"error": "Missing username or password"}), 400

    if username == "admin" and password == "secure_password":
        logger.info(f"Successful login for user: {username}", extra={"user": username})
        return jsonify({"message": "Login successful", "token": "mock-jwt-token"}), 200
    else:
        logger.warning(f"Failed login attempt for user: {username}", extra={
            "username": username,
            "ip": request.remote_addr
        })
        return jsonify({"error": "Invalid credentials"}), 401

# --- Payment Endpoint with Circuit Breaker ---
@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    
    # 1. Kiểm tra payload (Validation)
    if not data or 'amount' not in data:
        logger.warning("Payment request missing amount", extra={"payload": data})
        return jsonify({"error": "Missing amount in payload"}), 400
    
    amount = data.get('amount')
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Invalid amount", "value": amount}), 400

    try:
        logger.info(f"Initiating payment request of {amount} to external gateway")
        
        # 2. Giả lập Gateway lỗi nếu amount là một số đặc biệt (ví dụ 999)
        if amount == 999:
            # Gọi hàm giả lập lỗi được bọc bởi circuit breaker
            return call_faulty_gateway()
            
        result = call_external_payment_gateway()
        return jsonify(result), 200
    except CircuitBreakerError:
        # Mạch đang mở (Open)
        logger.error("Circuit Breaker is OPEN! Blocking requests to Payment Gateway.")
        return jsonify({
            "status": "error",
            "message": "Hệ thống thanh toán đang bảo trì (Circuit Open). Vui lòng thử lại sau.",
            "fallback": True
        }), 503
    except Exception as e:
        # Lỗi từ gateway
        logger.warning(f"Payment Gateway call failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@circuit(failure_threshold=5, recovery_timeout=30)
def call_faulty_gateway():
    """Hàm luôn trả về lỗi để test Circuit Breaker nhanh"""
    time.sleep(1)
    raise Exception("Critical Gateway Error (Simulated)")

# --- Admin Endpoint to toggle Gateway status (For Testing) ---
@app.route('/api/admin/toggle-gateway', methods=['POST'])
def toggle_gateway():
    global PAYMENT_GATEWAY_UP
    PAYMENT_GATEWAY_UP = not PAYMENT_GATEWAY_UP
    status = "UP" if PAYMENT_GATEWAY_UP else "DOWN"
    logger.info(f"Admin toggled Payment Gateway status to: {status}")
    return jsonify({"gateway_status": status}), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning("Rate limit exceeded", extra={
        "ip": request.remote_addr,
        "path": request.path,
        "description": str(e.description)
    })
    return jsonify({
        "error": "Too Many Requests",
        "message": "Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau 15 phút.",
        "description": e.description
    }), 429

if __name__ == '__main__':
    logger.info("Starting Flask Server on port 5000 with Circuit Breaker")
    app.run(debug=True, port=5000)
