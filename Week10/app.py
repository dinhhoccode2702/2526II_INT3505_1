from flask import Flask, jsonify, request
from logger_config import logger
import traceback

app = Flask(__name__)

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
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Login attempt missing credentials", extra={
            "path": request.path,
            "ip": request.remote_addr
        })
        return jsonify({"error": "Missing username or password"}), 400

    # Mock logic
    if username == "admin" and password == "secure_password":
        logger.info(f"Successful login for user: {username}", extra={"user": username})
        return jsonify({"message": "Login successful", "token": "mock-jwt-token"}), 200
    else:
        logger.warn(f"Failed login attempt for user: {username}", extra={
            "username": username,
            "ip": request.remote_addr
        })
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/error', methods=['GET'])
def trigger_error():
    """Endpoint to test error logging"""
    try:
        # Simulate a crash
        result = 1 / 0
    except Exception as e:
        logger.error("A critical error occurred in /api/error", extra={
            "exception": str(e),
            "stacktrace": traceback.format_exc()
        })
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    logger.info("Starting Flask Server on port 5000")
    app.run(debug=True, port=5000)
