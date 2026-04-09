# 📘 RAML - Library API: Hướng dẫn sinh server Flask từ `.raml`

Mục tiêu: từ `raml/library-api.raml` sinh ra một server stub (Flask) có thể chạy được, và đặt kết quả vào `out/raml/flask-server`.

## Tổng quan luồng công việc
- 1) Chuyển RAML → OpenAPI (RAML ít được OpenAPI Generator hỗ trợ trực tiếp).
- 2) Dùng OpenAPI Generator để sinh server Python (Flask) từ OpenAPI kết quả.

---

## Yêu cầu phần mềm (Windows PowerShell)
- Node.js & npm
- Java 11+ (nếu không dùng Docker)
- (Tùy chọn) Docker

## Công cụ sẽ dùng
- `raml2openapi` (npx) — chuyển RAML → OpenAPI
- `@openapitools/openapi-generator-cli` (npx hoặc Docker) — sinh server từ OpenAPI

---

## 1) Chuyển `raml/library-api.raml` → `openapi/library-from-raml.yaml`

Mở PowerShell tại thư mục repo root (`C:\Users\ADMIN\OneDrive\Desktop\KTHDV`) và chạy:

```powershell
# dùng npx (không cần cài global)
npx raml2openapi raml/library-api.raml openapi/library-from-raml.yaml --pretty

# nếu muốn cài global
# npm install -g raml2openapi
# raml2openapi raml/library-api.raml openapi/library-from-raml.yaml --pretty
```

Nếu thành công bạn sẽ thấy file `openapi/library-from-raml.yaml` được tạo.

---

## 2) Sinh Flask server stub từ OpenAPI

Hai cách: dùng `npx` (không cần Java) hoặc Docker image (không cần Java cục bộ).

- Cách A (npx wrapper):

```powershell
npx @openapitools/openapi-generator-cli generate -i openapi/library-from-raml.yaml -g python-flask -o out/raml/flask-server
```

- Cách B (Docker):

```powershell
docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate -i /local/openapi/library-from-raml.yaml -g python-flask -o /local/out/raml/flask-server
```

Sau khi chạy, thư mục `out/raml/flask-server` sẽ chứa scaffold server.

---

## 3) Thiết lập môi trường Python và chạy server (PowerShell)

```powershell
cd out/raml/flask-server

# tạo virtualenv
python -m venv .venv

# nếu PowerShell chặn script (chỉ lần đầu)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

# activate venv
. .\.venv\Scripts\Activate.ps1

# cài dependencies (nếu generator có requirements.txt)
if (Test-Path requirements.txt) { pip install -r requirements.txt } else { pip install flask }

# chạy server: kiểm tra README trong folder sinh ra; thường thử:
python -m openapi_server

# nếu không chạy được, mở out/raml/flask-server/README.md và làm theo hướng dẫn trong đó.
```

---

## 4) Kiểm tra endpoint

```powershell
curl http://localhost:8080/books
```

Hoặc dùng Postman/Swagger UI trỏ tới `http://localhost:8080`.

---

## 5) Troubleshooting nhanh

- Nếu `npx raml2openapi` báo lỗi parse RAML: mở `raml/library-api.raml` và kiểm tra cú pháp YAML (indent, `types`, `uriParameters`).
- Nếu OpenAPI Generator báo lỗi khi generate: validate OpenAPI bằng `swagger-cli`:

```powershell
npx @apidevtools/swagger-cli validate openapi/library-from-raml.yaml
```
- Nếu bạn không có Java: dùng Docker command (Cách B) để generate.
- Nếu server không start: đọc `out/raml/flask-server/README.md` để biết entrypoint chính xác; tìm package tên `openapi_server` hoặc file `__main__.py`.

---

## 6) Tùy biến sau khi sinh scaffold

- Scaffold chỉ là stub — bạn cần implement logic trong handlers/controllers.
- Thêm cấu hình `securitySchemes` vào OpenAPI nếu cần auth, hoặc tích hợp auth vào code sinh ra.

---

Nếu bạn muốn, tôi có thể chạy các lệnh trên (convert + generate) ngay bây giờ và tạo `out/raml/flask-server` trong repo, rồi hướng dẫn bạn chạy cụ thể. Nói "Làm đi" để tôi bắt đầu.
