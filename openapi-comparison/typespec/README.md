# 📘 TypeSpec - Library API

## 🔍 Giới thiệu tổng quan

**TypeSpec** (trước đây là Cadl) là một ngôn ngữ mô tả API thế hệ mới do Microsoft phát triển, mang triết lý thiết kế "Code-first". 

Thay vì phải vật lộn với các file OpenAPI (Swagger) định dạng YAML/JSON nguyên khối, dài dòng và dễ sai thụt lề, TypeSpec mang đến trải nghiệm thiết kế API nhẹ nhàng hơn rất nhiều. Nó hoạt động như một **Trình biên dịch (Compiler)**: lập trình viên định nghĩa cấu trúc API bằng cú pháp quen thuộc giống TypeScript, sau đó TypeSpec sẽ tự động biên dịch (compile) bản thiết kế này ra các chuẩn phổ quát như OpenAPI 3.0, JSON Schema hoặc Protobuf.

**Điểm nhấn cốt lõi:**
* Cú pháp thuần lập trình (TypeScript-like).
* Xóa bỏ sự cồng kềnh của YAML.
* Thiết kế hướng Module (chia nhỏ và tái sử dụng code dễ dàng).

---

## 📂 File trong thư mục
* `library-api.tsp`: File định nghĩa API gốc bằng ngôn ngữ TypeSpec.

---

## ⚙️ Cài đặt & Chạy
*Lưu ý: TypeSpec là ngôn ngữ thiết kế và biên dịch, không có tool tích hợp để gửi request test trực tiếp. Do đó, quy trình bắt buộc là phải chuyển đổi sang tài liệu YAML rồi mới tiến hành test.*

**Bước 1: Cài đặt Node.js**
Đảm bảo máy của bạn đã cài Node.js (kèm theo `npm`).
- Tải tại: https://nodejs.org/

**Bước 2: Cài đặt TypeSpec và thư viện**
Mở terminal tại thư mục dự án và chạy lần lượt 2 lệnh sau:
- Cài trình biên dịch (global): 
  `npm install -g @typespec/compiler`
- Cài các thư viện chuẩn REST và OpenAPI vào dự án:
  `npm install @typespec/http @typespec/rest @typespec/openapi @typespec/openapi3`

**Bước 3: Compile sang OpenAPI**
Chạy lệnh biên dịch (lưu ý truyền đúng tên file và cờ emit):
`tsp compile library-api.tsp --emit @typespec/openapi3`

Sau khi compile thành công, hệ thống sẽ sinh ra file YAML tại:
`tsp-output/@typespec/openapi3/openapi.yaml`

**Bước 4: Xem và Test bằng Swagger**
1. Truy cập: https://editor.swagger.io/
2. Mở file `openapi.yaml` vừa sinh ra, copy toàn bộ nội dung và dán vào khung bên trái của Swagger.
3. Xem giao diện API bên phải và bấm "Try it out" để test trực tiếp.

---

## 🚀 Ưu điểm

* **Thân thiện với Developer:** Cú pháp giống hệt TypeScript/C#, giúp lập trình viên đọc hiểu và viết tài liệu cực kỳ nhanh chóng mà không cần học cú pháp mới.
* **Tái sử dụng & Module hóa:** Khắc phục triệt để điểm yếu của OpenAPI. Hỗ trợ kế thừa (extends), tạo custom Models, Decorators và Aliases, giúp tách nhỏ file và không bị lặp lại code (DRY - Don't Repeat Yourself).
* **Hỗ trợ IDE mạnh mẽ:** Khi dùng extension trên VS Code, nó hỗ trợ auto-complete, highlight syntax và bắt lỗi logic realtime ngay lúc đang gõ.
* **Đa mục tiêu (Multi-target):** Một file TypeSpec duy nhất có thể sinh ra đồng thời nhiều chuẩn đầu ra (OpenAPI cho REST, Protobuf cho gRPC).

## ❌ Nhược điểm

* **Thiếu công cụ Test trực tiếp:** Không thể bấm test ngay trên file `.tsp`, buộc phải tốn thêm một bước biên dịch (compile) trung gian ra file YAML/JSON.
* **Hệ sinh thái đang phát triển:** Là công nghệ khá mới, cộng đồng chưa lớn mạnh bằng OpenAPI, do đó tài liệu hướng dẫn fix lỗi (troubleshooting) trên mạng còn hạn chế.