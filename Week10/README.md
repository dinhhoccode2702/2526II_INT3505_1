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

## Tại sao Log JSON lại quan trọng?
Các hệ thống quản lý log hiện đại như **ELK Stack (Elasticsearch, Logstash, Kibana)**, **Datadog**, hoặc **CloudWatch** có thể dễ dàng parse log JSON để phân tích, vẽ biểu đồ và thiết lập cảnh báo tự động mà không cần dùng các Regex phức tạp.
