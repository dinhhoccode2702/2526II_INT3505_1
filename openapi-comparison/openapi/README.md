# Hướng dẫn xử lý OpenAPI (*.yaml/*.json)

## 1. Công cụ & Thư viện hỗ trợ
- **OpenAPI Generator CLI**: Trình tạo code server/client mạnh mẽ và phổ biến nhất thế giới hiện tại (Khuyên dùng thay thế hoàn toàn cho Swagger Codegen cũ).
- **Swagger UI / Redoc**: Thư viện sinh giao diện đọc Document trên Web.
- **Swagger Editor**: Trình soạn thảo trực tuyến giúp check lỗi syntax YAML.

## 2. Quy trình sinh Server Backend trực tiếp
Vì đây là định dạng OpenAPI chuẩn gốc, chúng ta có thể sinh code ngay lập tức mà không qua bước biên dịch trung gian, hỗ trợ hàng chục ngôn ngữ (Python, Node.js, Go, Java...).

### Bước 1: Sinh code server (Yêu cầu Node.js)
Mở terminal tại thư mục này để sinh ra backend Python Flask:
```bash
npx @openapitools/openapi-generator-cli generate -i library.yaml -g python-flask -o ./library-backend
```
*(Lưu ý: Nếu không có npx/node.js, bạn có thể thay thế bằng file java `swagger-codegen-cli.jar`)*.

### Bước 2: Cài đặt thư viện cho server vừa sinh ra
```bash
cd library-backend
pip install -r requirements.txt
```

### Bước 3: Khởi chạy Server
```bash
python -m openapi_server
```
Đường dẫn giao diện API cục bộ sẽ được mở tại: `http://localhost:8080/ui`