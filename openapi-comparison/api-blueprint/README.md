# Hướng dẫn xử lý API Blueprint (*.apib)

## 1. Công cụ & Thư viện hỗ trợ
- **Drakov / Snowboard**: Dùng để chạy Mock Server nhanh từ file `.apib`.
- **Aglio**: Dùng để build ra trang tài liệu HTML trực quan.
- **apib2swagger**: Chuyển đổi từ API Blueprint sang OpenAPI.
- **OpenAPI Generator**: Trình sinh code server chuyên nghiệp.

## 2. Quy trình sinh Server Backend
Bản chất API Blueprint rất khó gen trực tiếp ra code backend chất lượng. Cách tiếp cận chuẩn và hiện đại nhất hiện nay là **chuyển đổi sang chuẩn OpenAPI** rồi xài công cụ Gen code của OpenAPI.

### Bước 1: Cài đặt công cụ chuyển đổi (Yêu cầu Node.js)
```bash
npm install -g apib2swagger
```

### Bước 2: Chuyển đổi sang OpenAPI
```bash
npx apib2swagger -i library-api.apib -o openapi.yaml
```

### Bước 3: Dùng OpenAPI Generator để sinh code Server
Sử dụng file YAML vừa được tạo ra để sinh ra server bằng Python Flask:
```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./backend-server
```

### Bước 4: Cài đặt và Chạy server
Đi vào thư mục vừa gen ra và cài đặt thư viện khởi chạy:
```bash
cd backend-server
pip install -r requirements.txt
python -m openapi_server
```