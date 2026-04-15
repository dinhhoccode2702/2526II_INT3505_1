# Hướng dẫn xử lý TypeSpec (*.tsp)

## 1. Công cụ & Thư viện hỗ trợ
- **TypeSpec Compiler (`tsp`)**: Trình biên dịch của Microsoft. Giúp viết code mô tả thiết kế API như đang viết code TypeScript.
- **@typespec/openapi3**: Thư viện Emitter đi kèm để biên dịch mã TypeSpec sang file chuẩn OpenAPI 3.
- **VS Code Extension (TypeSpec)**: Phải cài Extension này trên Visual Studio Code để được báo lỗi cú pháp và gợi ý code tự động.

## 2. Quy trình dịch và sinh Server Backend
Mục tiêu cốt lõi của TypeSpec là "Dùng ngôn ngữ lập trình để sinh ra file đặc tả". TypeSpec không trực tiếp gen ra Backend, mà nó **Biên dịch (Compile)** file `.tsp` bắn ra file trung gian `openapi.yaml` cực chuẩn xác.

### Bước 1: Khởi tạo và Cài đặt Compiler TypeSpec
Mở terminal tại thư mục này và tải compiler:
```bash
npm install -g @typespec/compiler
npm install @typespec/openapi3
```

### Bước 2: Biên dịch TypeSpec sang OpenAPI
Do trong command compile ta cần bảo cho `tsp` biết format đích mà ta cần sinh ra là gì, nên bạn phải thêm cờ `--emit @typespec/openapi3` vào như sau:
```bash
npx tsp compile library-api.tsp --emit @typespec/openapi3
```
*(Sau lệnh này, hệ thống sẽ báo `No errors` rồi nhả ra một cấu trúc thư mục chứa file yaml: `tsp-output/@typespec/openapi3/openapi.yaml`)*.

### Bước 3: Sử dụng file YAML đó để sinh Server Backend
Chạy tool Gen code trỏ tới đúng file YAML vừa thu được:
```bash
npx @openapitools/openapi-generator-cli generate -i ./tsp-output/@typespec/openapi3/openapi.yaml -g python-flask -o ./typespec-backend
```

### Bước 4: Cài đặt và chạy Server
```bash
cd typespec-backend
pip install -r requirements.txt
python -m openapi_server
```