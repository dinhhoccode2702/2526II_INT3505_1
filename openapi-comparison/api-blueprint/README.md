# 📘 API Blueprint - Library API

## 🔍 Giới thiệu tổng quan

**API Blueprint** là một ngôn ngữ thiết kế API cấp cao, được xây dựng hoàn toàn dựa trên cú pháp **Markdown** quen thuộc (cụ thể hơn là sử dụng MSON - Markdown Syntax for Object Notation cho phần mô tả dữ liệu).

Triết lý cốt lõi của API Blueprint là **Documentation-Driven Design (Tài liệu đi trước)**. Khác với OpenAPI (Swagger) hay định dạng JSON vốn nặng về tính kỹ thuật và tối ưu cho máy đọc (machine-readable), API Blueprint đặt trải nghiệm của **con người (human-readable)** lên hàng đầu. Nó giống như việc bạn đang viết một bài blog hoặc một file README kể một câu chuyện về cách API của bạn hoạt động.

**Điểm nhấn cốt lõi:**
* Cú pháp Markdown thuần túy, cực kỳ dễ học, dễ đọc.
* Là công cụ giao tiếp hoàn hảo giữa đội ngũ Kỹ thuật (Dev) và đội ngũ Kinh doanh (Business/Client) vì ai nhìn vào cũng hiểu được.
* Tài liệu sinh ra (Render) có giao diện hiển thị cực kỳ đẹp mắt và phân bổ thông tin rõ ràng.

---

## 📂 File trong thư mục
* `library-api.apib`: File gốc mô tả toàn bộ tài liệu API Quản lý sách theo định dạng API Blueprint.

---

## ⚙️ Cài đặt & Kiểm thử (Testing)

API Blueprint hỗ trợ render tài liệu và test trực tiếp, nhưng hệ sinh thái của nó phụ thuộc khá nhiều vào nền tảng **Apiary**.

**Sử dụng Apiary Platform (Nhanh nhất)**
1. Truy cập: [Apiary Editor](https://app.apiary.io/) (Yêu cầu đăng nhập).
2. Tạo một project mới và dán toàn bộ nội dung file `library-api.apib` vào khung soạn thảo.
3. Apiary sẽ tự động render ra một trang tài liệu rất đẹp bên phải.
4. **Để Test API:** Chuyển sang chế độ **Console** trên tài liệu, bạn có thể gọi API thử. 
   * *Lưu ý thực chiến:* Hệ thống Proxy của Apiary khá cũ và thường lỗi khi gọi API ra các domain ngoài (như Vercel hoặc Localhost). Tốt nhất bạn nên chọn môi trường **Mock Server** để Apiary tự động trả về dữ liệu mẫu mà không cần kết nối tới Backend thực.

## 🚀 Ưu điểm

* **Learning Curve cực thấp:** Bất kỳ ai biết viết Markdown đều có thể viết được API Blueprint trong vài chục phút làm quen.
* **Đọc hiểu không rào cản:** Code viết ra nhìn y hệt như tài liệu văn bản, không bị nhiễu bởi các dấu `{ }`, `[ ]` hay lùi lề khắt khe như JSON/YAML.
* **Hỗ trợ Mocking tự động tốt:** Trên Apiary, ngay khi bạn gõ xong định dạng Response, hệ thống lập tức tạo ra một Mock Server để Frontend có thể lấy link gọi API thử luôn mà không cần chờ Backend code xong.

## ❌ Nhược điểm

* **Hệ sinh thái đang lụi tàn (Declining Ecosystem):** Nền tảng chính chủ là Apiary (đã bị Oracle mua lại) đã chính thức có thông báo **End of Life (Ngừng hoạt động) vào tháng 10/2026**. Điều này khiến tương lai của API Blueprint khá mờ mịt.
* **Thiếu công cụ tự động hóa:** Rất yếu trong việc tự động sinh mã nguồn (Codegen) cho Client/Server so với OpenAPI.
* **Validation lỏng lẻo:** Do tính chất văn bản của Markdown, việc ràng buộc chặt chẽ kiểu dữ liệu (Schema Validation) hay các rule phức tạp (như regex, min/max) khó khăn và không tiêu chuẩn hóa tốt bằng OpenAPI.