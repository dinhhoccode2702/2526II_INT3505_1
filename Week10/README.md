# Week 10: Phase 1 - Foundation & Logging

Giai đoạn này tập trung vào việc xây dựng một Base API bằng Flask và thiết lập hệ thống Logging có cấu trúc (Structured Logging) - một kỹ năng quan trọng cho Senior/DevOps Engineer.

## Các thành phần chính

1.  **Base API (Flask)**:
    - `GET /api/users`: Trả về danh sách user.
    - `POST /api/login`: Xử lý đăng nhập (mock).
    - `GET /api/error`: Endpoint mô phỏng lỗi để kiểm tra logging.

2.  **Structured Logging (JSON)**:
    - Sử dụng `python-json-logger` để tạo log định dạng JSON.
    - **Levels**:
        - `INFO`: Ghi lại các hoạt động bình thường của hệ thống.
        - `WARN`: Cảnh báo các hành vi đáng ngờ (ví dụ: login thất bại).
        - `ERROR`: Ghi lại lỗi exception kèm theo stacktrace.
    - **Transports**:
        - **Console**: Hiển thị log trực tiếp khi dev.
        - **app.log**: Lưu trữ tất cả các log từ mức INFO trở lên.
        - **error.log**: Chỉ lưu trữ các log mức ERROR (giúp DevOps dễ dàng filter lỗi).

3.  **Rate Limiting (Bảo vệ API)**:
    - Sử dụng `Flask-Limiter` để ngăn chặn spam và Brute-force attacks.
    - **Rule cơ bản**: Giới hạn 100 requests / 15 phút cho mỗi IP (áp dụng toàn hệ thống).
    - **Rule nghiêm ngặt**: Áp dụng cho `/api/login` - chỉ cho phép 5 lần thử / 15 phút để chống Brute-force.
    - **Custom Error**: Khi vượt quá giới hạn, API sẽ trả về HTTP `429 Too Many Requests` và ghi log cảnh báo.

4.  **Circuit Breaker (Chống treo hệ thống)**:
    - Sử dụng thư viện `circuitbreaker` để bảo vệ ứng dụng khi API bên thứ 3 (Payment Gateway) gặp sự cố.
    - **Cơ chế**: Nếu gọi API bên ngoài lỗi 5 lần liên tiếp, mạch sẽ **Mở (Open)**.
    - Khi mạch Mở: Mọi request tiếp theo sẽ bị từ chối ngay lập tức (trả về fallback data) mà không cần chờ timeout, giúp giải phóng tài nguyên hệ thống.
    - Sau 30 giây, mạch sẽ chuyển sang **Half-Open** để thử gọi lại API bên ngoài.

5.  **Monitoring (Giám sát hệ thống)**:
    - Sử dụng `prometheus-flask-exporter` để xuất dữ liệu metrics.
    - **Endpoint `/metrics`**: Cung cấp dữ liệu về:
        - Số lượng HTTP Request (theo method, status code, path).
        - Thời gian phản hồi của API (Response time).
        - Thông tin hệ thống (CPU, RAM usage).
    - Dữ liệu này tuân thủ chuẩn Prometheus, có thể dùng để tích hợp vào các hệ thống giám sát.

## Hướng dẫn chạy

1.  Cài đặt thư viện:
    ```bash
    pip install -r requirements.txt
    ```

2.  Chạy ứng dụng:
    ```bash
    python app.py
    ```

3.  Kiểm tra file `app.log` và `error.log` được tạo ra trong thư mục `Week10`.

## Hướng dẫn Test Rate Limiting

### Cách 1: Sử dụng Postman (Thủ công)
1.  Mở Postman, tạo request `POST` đến `http://127.0.0.1:5000/api/login`.
2.  Trong phần **Body**, chọn `raw` và `JSON`, nhập: `{"username": "admin", "password": "wrong_password"}`.
3.  Nhấn **Send** liên tục 6 lần.
4.  Ở lần thứ 6, bạn sẽ nhận được mã lỗi `429 Too Many Requests`.

### Cách 2: Sử dụng Command Line (Nhanh)
Nếu bạn có `curl` (Windows/Linux/Mac), hãy chạy lệnh sau để gửi 6 request liên tục:
```bash
for /l %i in (1,1,6) do curl -X POST http://127.0.0.1:5000/api/login -H "Content-Type: application/json" -d "{\"username\":\"admin\", \"password\":\"123\"}"
```
*(Lưu ý: Nếu dùng Bash/Linux thì thay bằng: `for i in {1..6}; do curl ...; done`)*

### Quan sát kết quả trong Log
Sau khi bị chặn, hãy mở file `app.log`. Bạn sẽ thấy một dòng log dạng JSON với nội dung `"message": "Rate limit exceeded"`, đây là bằng chứng hệ thống đã tự bảo vệ thành công.

## Hướng dẫn Test Circuit Breaker

### Bước 1: Gọi API khi Gateway đang hoạt động (Bình thường)
Gửi request `POST` đến `http://127.0.0.1:5000/api/payment`. Bạn sẽ nhận được `status: success`.

### Bước 2: Giả lập Gateway bị sập (Admin Action)
Gửi request `POST` đến `http://127.0.0.1:5000/api/admin/toggle-gateway`. 
Kết quả trả về sẽ là `gateway_status: DOWN`.

### Bước 3: Kích hoạt ngắt mạch (Tripping the Circuit)
1. Gửi request `POST` đến `http://127.0.0.1:5000/api/payment` liên tục.
2. 5 lần đầu: Bạn sẽ phải chờ 2 giây (giả lập timeout) và nhận lỗi `500`.
3. Từ lần thứ 6: Bạn sẽ nhận được phản hồi **ngay lập tức** (không chờ 2s) với mã lỗi `503` và message `"Hệ thống thanh toán đang bảo trì (Circuit Open)"`. 
4. Lúc này mạch đã **Mở (Open)** để bảo vệ server của bạn không bị treo tài nguyên.

### Bước 4: Chờ phục hồi (Half-Open)
Chờ 30 giây, sau đó gửi lại request. Mạch sẽ thử gọi lại Gateway một lần nữa.

## Hướng dẫn xem Metrics

### Bước 1: Truy cập endpoint metrics
Mở trình duyệt và truy cập: `http://127.0.0.1:5000/metrics`

### Bước 2: Đọc dữ liệu
Bạn sẽ thấy một danh sách dài các text. Đây là định dạng chuẩn của Prometheus. Hãy tìm các dòng quan trọng:
- `flask_http_request_total`: Tổng số request đã gửi đến API.
- `flask_http_request_duration_seconds`: Thời gian xử lý request.
- `process_virtual_memory_bytes`: Lượng RAM ứng dụng đang sử dụng.

> [!TIP]
> **Giải đáp về Grafana/Docker**: Bạn **KHÔNG BẮT BUỘC** phải dùng Grafana hay Docker. Endpoint `/metrics` xuất dữ liệu chuẩn Prometheus dưới dạng text. Bạn có thể xem trực tiếp bằng trình duyệt để kiểm tra thông số hệ thống. Grafana chỉ cần khi bạn muốn vẽ biểu đồ trực quan.

## Hướng dẫn Test JWT Authentication

### Bước 1: Đăng nhập để lấy Token
Gửi `POST` đến `/api/login` với thông tin:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
Bạn sẽ nhận được một chuỗi `token` dài (JWT).

### Bước 2: Truy cập Endpoint bảo mật
Gửi `GET` đến `/api/profile`.
- **Nếu không có token**: Bạn nhận lỗi `401 Unauthorized`.
- **Nếu có token**: Thêm Header `Authorization: Bearer <token_cua_ban>`. Bạn sẽ nhận được thông tin cá nhân.

## Tại sao Log JSON lại quan trọng?
Các hệ thống quản lý log hiện đại như **ELK Stack (Elasticsearch, Logstash, Kibana)**, **Datadog**, hoặc **CloudWatch** có thể dễ dàng parse log JSON để phân tích, vẽ biểu đồ và thiết lập cảnh báo tự động mà không cần dùng các Regex phức tạp.
