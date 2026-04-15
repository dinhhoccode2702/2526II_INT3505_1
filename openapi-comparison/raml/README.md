# Hướng dẫn xử lý RAML (*.raml)

## 1. Công cụ & Thư viện hỗ trợ
- **Osprey**: Chạy Mock Server trực tiếp từ file RAML (dành riêng cho Node.js).
- **raml2html**: Render trực tiếp file `.raml` ra trang Website dạng HTML để dễ đọc tài liệu.
- **oas-raml-converter**: Công cụ biên dịch từ RAML sang chuẩn OpenAPI.

## 2. Quy trình sinh Server Backend
Giống như API Blueprint, RAML ngày nay đã được hệ sinh thái Gen code hỗ trợ trực tiếp một cách mạnh mẽ. Giải pháp tối ưu nhất là **Biên dịch file RAML về chuẩn OpenAPI 3.0**.

### Bước 1: Cài đặt bộ chuyển đổi (Yêu cầu Node.js)
Cài đặt công cụ chuyển từ RAML về OpenAPI:
```bash
npm install -g oas-raml-converter
```

### Bước 2: Ép kiểu RAML sang OpenAPI 3.0
Do công cụ này in trực tiếp kết quả ra màn hình (terminal), nên ta cần dùng dấu `>` để ghi đè kết quả đó vào file `openapi.yaml`.

Trên Terminal (Cmd/Bash):
```bash
```powershell
npx oas-raml-converter --from RAML --to OAS30 library-api.raml | Out-File -Encoding utf8 openapi.yaml
```

### Bước 3: Sử dụng OpenAPI Generator để sinh code Server
Một khi đã có file `openapi.yaml` trong tay, chạy trình Gen code tiêu chuẩn:
```bash
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./raml-backend
```
npx @openapitools/openapi-generator-cli generate -i openapi.yaml -g python-flask -o ./raml-backend

### Bước 4: Chạy server
```bash
cd raml-backend
pip install -r requirements.txt
python -m openapi_server
```