# Week 4 - Book API (Flask + Vercel)

## Deploy Link
- Production: https://2526-ii-int-3505-1-gpf3.vercel.app/

## Mô Tả
Dự án xây dựng REST API quản lý sách bằng Flask.
API hỗ trợ CRUD và tìm kiếm sách theo tiêu đề.

## Công Nghệ
- Python
- Flask
- flask-cors
- Vercel Serverless Functions

## Cấu Trúc Thư Mục
- server.py: Flask app chính
- openAPI_book.yaml: Đặc tả OpenAPI
- requirements.txt: Danh sách dependencies
- vercel.json: Cấu hình deploy Vercel

## API Endpoints
Base URL production:
https://2526-ii-int-3505-1-gpf3.vercel.app

1. GET /api/v1/books
- Lấy danh sách sách

2. GET /api/v1/books/{book_id}
- Lấy chi tiết sách theo id

3. GET /api/v1/books/search?title=<keyword>
- Tìm sách theo title

4. POST /api/v1/books
- Tạo sách mới
- Body JSON mẫu:
{
  "title": "Refactoring",
  "author": "Martin Fowler",
  "genre": "Programming",
  "published_year": 1999,
  "price": 20.5,
  "is_available": true
}

5. PUT/PATCH /api/v1/books/{book_id}
- Cập nhật toàn bộ hoặc một phần thông tin sách

6. DELETE /api/v1/books/{book_id}
- Xóa sách

## Ghi Chú
- Dữ liệu đang in-memory (list books trong server.py), nên sẽ reset sau mỗi lần deploy/restart.
- OpenAPI file hiện tại là openAPI_book.yaml.
