# 📘 OpenAPI (Swagger) - Library API

## 🔍 Giới thiệu tổng quan

**OpenAPI Specification (OAS)** (trước đây được biết đến với tên gọi Swagger) hiện là chuẩn mô tả RESTful API phổ biến và quyền lực nhất thế giới (De facto standard). 

OpenAPI định nghĩa một ngôn ngữ chung, độc lập với nền tảng lập trình, cho phép cả con người và máy tính khám phá và hiểu được các chức năng của dịch vụ mà không cần truy cập vào mã nguồn (source code). Nó đóng vai trò như một **Bản hợp đồng API (API Contract)** vững chắc giữa Backend, Frontend và các đối tác tích hợp (Third-party).

**Điểm nhấn cốt lõi:**
* Cấu trúc dựa trên YAML hoặc JSON, tuân thủ chặt chẽ các quy tắc của JSON Schema.
* Tự động hóa toàn diện: từ sinh giao diện tài liệu (Swagger UI), sinh mã nguồn (Codegen) cho đến kiểm thử tự động.
* Được hỗ trợ bởi tất cả các Cloud Provider lớn (AWS, Google Cloud, Azure) và các API Gateway.



---

## 📂 File trong thư mục
* `library.yaml`: File đặc tả toàn bộ cấu trúc API Quản lý sách (endpoints, parameters, request/response bodies, security) theo chuẩn OpenAPI 3.0.

---

## ⚙️ Cài đặt & Kiểm thử (Testing)

Khác với TypeSpec phải qua biên dịch, OpenAPI sở hữu hệ sinh thái công cụ hỗ trợ **kiểm thử trực tiếp (Live Testing)** mạnh mẽ nhất hiện nay.

**Sử dụng Swagger Editor**
1. Truy cập: [Swagger Editor](https://editor.swagger.io/).
2. Copy toàn bộ nội dung file `library.yaml` và dán vào khung soạn thảo bên trái.
3. Khung bên phải sẽ tự động render ra giao diện **Swagger UI** cực kỳ trực quan.
4. Mở rộng bất kỳ endpoint nào (VD: `POST /books`), nhấn nút **"Try it out"**, điền tham số và bấm **"Execute"** để gửi request thực tế xuống server.


## 🚀 Ưu điểm

* **Tiêu chuẩn công nghiệp (Industry Standard):** Độ phổ biến tuyệt đối. Gần như mọi framework backend (Spring Boot, FastAPI, NestJS) đều có thư viện tự động sinh ra file OpenAPI từ code.
* **Hệ sinh thái Tooling khổng lồ:** Hỗ trợ OpenAPI Generator để tự động sinh Client SDK (React, Angular, Vue) hoặc Server Stubs (Node, PHP, Java) chỉ với 1 câu lệnh, tiết kiệm hàng tuần làm việc.
* **Ràng buộc dữ liệu chặt chẽ (Strict Validation):** Định nghĩa cấu trúc dữ liệu rất chi tiết (từ data type, regex, đến min/max length), giúp API Gateway tự động chặn các request sai định dạng trước khi chúng chạm tới Backend.

## ❌ Nhược điểm

* **Cú pháp dài dòng (Verbose) và dễ lỗi:** Định dạng YAML phụ thuộc hoàn toàn vào khoảng trắng (indentation). Ở các dự án lớn, một file OpenAPI có thể phình to lên hàng chục ngàn dòng, cực kỳ khó đọc bằng mắt thường và rất dễ bị lỗi cú pháp chỉ vì dư một dấu cách.
* **Khó bảo trì (Maintenance Overhead):** Nếu viết thủ công (Design-first) thay vì sinh ra từ code (Code-first), việc phải chia nhỏ file YAML ra nhiều file nhỏ (`$ref`) đòi hỏi kỹ năng quản lý cấu trúc thư mục phức tạp để công cụ không bị lỗi khi gộp lại.