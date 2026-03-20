# 📘 RAML - Library API

## 🔍 Giới thiệu tổng quan

**RAML (RESTful API Modeling Language)** là một ngôn ngữ mô hình hóa API dựa trên cú pháp YAML, do MuleSoft (hiện thuộc Salesforce) khởi xướng. 

Khác với OpenAPI thường mang tính chất "tài liệu hóa" các endpoint tĩnh, RAML mang đậm triết lý **Design-First (Thiết kế trước)** và định hướng theo **Tài nguyên (Resource-oriented)**. Nó cung cấp các cơ chế phân cấp dạng cây và khả năng kế thừa vô cùng mạnh mẽ, giúp các kiến trúc sư phần mềm (Software Architects) định hình rõ ràng cấu trúc của một hệ thống RESTful trước khi viết bất kỳ dòng code logic nào.

**Điểm nhấn cốt lõi:**
* Cấu trúc định tuyến phân cấp lồng nhau (Hierarchical routing).
* Tái sử dụng tối đa để tránh lặp code (DRY - Don't Repeat Yourself).
* Rất phù hợp cho các hệ thống Enterprise quy mô lớn.



---

## 📂 File trong thư mục
* `library-api.raml`: File gốc mô tả cấu trúc API Quản lý sách theo chuẩn RAML 1.0.

---

## ⚙️ Cài đặt & Kiểm thử (Testing)

Khác với TypeSpec, RAML **có hỗ trợ công cụ để gửi request test trực tiếp** từ giao diện tài liệu thông qua API Console.

# Sử dụng Anypoint Platform
Đây là nền tảng đám mây của MuleSoft, cung cấp môi trường hoàn hảo nhất để thiết kế và test RAML.
1. Truy cập: [Anypoint Platform](https://anypoint.mulesoft.com/apiplatform/) và đăng nhập/đăng ký tài khoản miễn phí.
2. Điều hướng đến **Design Center** ➔ Tạo một "API Specification" mới.
3. Upload hoặc copy nội dung file `library-api.raml` vào trình soạn thảo.
4. Ở khung bên phải (API Console), bạn có thể xem giao diện tài liệu trực quan, bật tính năng **Mocking Service** và bấm nút **Send** để test API ngay lập tức.


---

## 🚀 Ưu điểm

* **Tái sử dụng code cực mạnh (Reusability):** Thông qua các khái niệm trừu tượng như `traits` (định nghĩa các hành vi chung như phân trang, lọc, xác thực) và `resourceTypes` (kiểu tài nguyên mẫu), RAML giúp giảm thiểu đáng kể số lượng dòng code so với OpenAPI.
* **Cấu trúc phân cấp trực quan:** URL được thiết kế lồng vào nhau (VD: `/books` ➔ chứa phương thức `get`, `post` ➔ lồng tiếp `/{id}` chứa `get`, `put`, `delete`). Cấu trúc này giúp người đọc nhìn file code là thấy ngay bức tranh tổng thể của hệ thống.
* **Tư duy Design-First chuẩn mực:** Ép lập trình viên phải tuân thủ nghiêm ngặt các quy tắc thiết kế RESTful bài bản.

## ❌ Nhược điểm

* **Độ phổ biến giảm sút:** Hiện nay OpenAPI (Swagger) đã thống trị thị trường mã nguồn mở, RAML đang dần bị thu hẹp và chủ yếu chỉ còn được dùng bởi các khách hàng doanh nghiệp nằm trong hệ sinh thái MuleSoft/Salesforce.
* **Learning Curve (Đường cong học tập) dốc:** Các khái niệm nâng cao như `traits`, `resourceTypes` hay `libraries` khá trừu tượng và khó tiếp cận với người mới bắt đầu hơn so với cấu trúc phẳng của OpenAPI.
* **Công cụ hỗ trợ (Tooling) hạn chế:** Ít công cụ mã nguồn mở hỗ trợ sinh code tự động (Codegen) hoặc làm tài liệu bên thứ ba so với hệ sinh thái khổng lồ của Swagger.