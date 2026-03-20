📘 TypeSpec - Library API
🔍 Giới thiệu

TypeSpec (trước đây là Cadl) là ngôn ngữ mới do Microsoft phát triển để mô tả API.

Điểm đặc biệt:

Cú pháp giống TypeScript

Có thể compile ra OpenAPI

Hướng tới developer-friendly

📂 File trong thư mục

main.tsp: File định nghĩa API bằng TypeSpec

⚙️ Cài đặt & chạy
Bước 1: Cài Node.js

https://nodejs.org/

Bước 2: Cài TypeSpec
npm install -g @typespec/compiler
Bước 3: Compile sang OpenAPI
tsp compile .

Sau khi compile, sẽ sinh ra:

tsp-output/@typespec/openapi3/openapi.yaml
Bước 4: Xem bằng Swagger

Mở file YAML bằng:

https://editor.swagger.io/
hoặc

Swagger UI local

🚀 Ưu điểm

Cú pháp giống code (TypeScript-like)

Dễ maintain với dev

Generate được OpenAPI

❌ Nhược điểm

Còn mới, chưa phổ biến

Cộng đồng nhỏ hơn OpenAPI