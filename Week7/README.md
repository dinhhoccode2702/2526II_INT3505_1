# Hướng dẫn tạo Backend Flask từ OpenAPI bằng Swagger Codegen và Kết nối MongoDB

Tài liệu này tóm tắt lại toàn bộ quy trình từ lúc thiết kế file `OpenAPISpec.yaml`, gen code tự động bằng Swagger Codegen, cho đến lúc cấu hình để Controller thực sự kết nối và lưu dữ liệu vào MongoDB.

---

## Bước 1: Tải công cụ Swagger Codegen
Bản chất Swagger Codegen là một file chạy Java (`.jar`). Mở Terminal (PowerShell) tại thư mục `Week7` và chạy lệnh sau để tải về:
```powershell
Invoke-WebRequest -OutFile swagger-codegen-cli.jar -Uri https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.52/swagger-codegen-cli-3.0.52.jar
```
*(Yêu cầu máy tính phải cài sẵn Java, kiểm tra bằng lệnh `java -version`)*.

---

## Bước 2: Sinh code Backend tự động
Khi đã có file `OpenAPISpec.yaml` và công cụ `swagger-codegen-cli.jar` trong cùng một thư mục `Week7`, chạy lệnh sau để tự động sinh code ra thư mục `book-backendd`:
```powershell
java -jar swagger-codegen-cli.jar generate -i OpenAPISpec.yaml -l python-flask -o ./book-backendd
```
> **Lưu ý Lỗi Encoding trên Windows:** Thỉnh thoảng PowerShell trên Windows tạo ra dư thừa các `Null bytes` trong các file rỗng (như `__init__.py`). Nếu chạy server báo lỗi `SyntaxError: source code string cannot contain null bytes`, hãy mở các file `__init__.py` lên, xóa trắng, chỉnh chuẩn Encoding sang `UTF-8` và lưu lại.

---

## Bước 3: Cài đặt thư viện
Di chuyển vào thư mục mới sinh ra và cài đặt các thư viện cần thiết, cộng thêm thư viện `mongoengine` để làm việc với MongoDB:
```powershell
cd book-backendd
pip install -r requirements.txt
pip install mongoengine
```

---

## Bước 4: 3 Thao tác "Phù phép" Code Gen thành Code Thật

Bản chất code do Swagger gen ra chỉ có xác, không có hồn (các hàm chỉ `return 'do some magic!'`). Để kết nối Database thật, bạn phải sửa 3 file sau:

### 4.1. Khai báo Kết nối Database (Sửa file `swagger_server/__main__.py`)
Mở file `__main__.py` và thêm kết nối MongoDB. **Đặc biệt lưu ý: Phải đặt lệnh kết nối TRƯỚC lệnh `app.run()`.**
```python
import connexion
from swagger_server import encoder
from mongoengine import connect  # 1. Thêm import này

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Book API'}, pythonic_params=True)
    
    # 2. Đặt kết nối MongoDB trước khi Server khởi chạy
    connect(host="mongodb://localhost:27017/book_manager")
    print("[OK] Da ket noi MongoDB thanh cong!")
    
    # Lệnh đóng băng CPU để hứng request (KHÔNG được để kết nối DB phía dưới lệnh này)
    app.run(port=8080)

if __name__ == '__main__':
    main()
```

### 4.2. Tạo Database Model cứng (Tạo file `swagger_server/models/book_db.py`)
Model Model do Swagger sinh ra (ví dụ `book.py`) chỉ là kiểu dữ liệu JSON để giao tiếp Web. Bạn phải tự tay tạo thêm một Model chuẩn của MongoEngine để giao tiếp với Ổ cứng máy chủ.
Tạo file mới `book_db.py`:
```python
from mongoengine import Document, StringField, FloatField, BooleanField, IntField

class BookDB(Document):
    meta = {'collection': 'books'} # Tên Data Collection trong MongoDB
    
    title = StringField(required=True)
    author = StringField(required=True)
    genre = StringField()
    published_year = IntField()
    price = FloatField()
    is_available = BooleanField(default=True)
```

### 4.3. Sửa Logic Controller (Sửa file `swagger_server/controllers/default_controller.py`)
Đây là thao tác cuối cùng và quan trọng nhất: Import Model DB vào và ghi đè logic rỗng.
**Lý do hay gặp lỗi:** Khi copy sang dự án mới, hãy chắc chắn thay đổi tên thư mục import gốc từ `OpenAPISpec` thành `swagger_server` (Tên package mặc định của công cụ Codegen).

Mẫu thay thế một hàm `POST` tạo Sách:
```python
import connexion
from swagger_server.models.book_response import BookResponse
from swagger_server.models.book_db import BookDB  # Import file Model database vừa làm ở trên

def api_v1_books_post(body): 
    """Tạo sách mới"""
    if connexion.request.is_json:
        req = connexion.request.get_json()
        try:
            # Gán dữ liệu request vào Schema MongoEngine
            new_book = BookDB(
                title=req.get('title'),
                author=req.get('author'),
                genre=req.get('genre'),
                published_year=req.get('published_year'),
                price=req.get('price'),
                is_available=True
            )
            # Lưu xuống Database thao tác thật!
            new_book.save() 
            return BookResponse(success=True, message="Created successfully"), 201
        except Exception as e:
            return str(e), 400
    return 'Invalid input', 400
```

---

## Bước 5: Chạy Server
Sau khi cấu hình xong, chỉ việc khởi động và tận hưởng:
```powershell
python -m swagger_server
```
Khởi chạy UI để dùng thử tại: **http://localhost:8080/ui**