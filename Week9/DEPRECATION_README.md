# Chiến lược quản lý Breaking Changes và Deprecation trong API

Khi hệ thống phát triển, việc thay đổi API là điều không thể tránh khỏi. Tuy nhiên, nếu thay đổi làm "gãy" (break) hệ thống của client đang sử dụng, đó gọi là **Breaking Change**. Quá trình cảnh báo và chuẩn bị khai tử một tính năng/endpoint cũ được gọi là **Deprecation**.

Dưới đây là chiến lược chuẩn xác và chuyên nghiệp để xử lý vấn đề này:

## 1. Breaking Changes là gì?
Các thay đổi sau đây được coi là "phá vỡ" tính tương thích ngược (backward compatibility) và cần quy trình Deprecation:
- Xóa bỏ một Endpoint, phương thức (GET, POST...) hoặc URL path.
- Đổi kiểu dữ liệu của một trường (ví dụ: `id` từ `integer` sang `string`).
- Xóa bỏ một trường trong JSON Response.
- Thay đổi cấu trúc của Request Payload (bắt buộc thêm một trường mới không có giá trị mặc định).
- Sửa đổi logic business làm thay đổi định dạng dữ liệu cốt lõi.

*Lưu ý:* Thêm một trường mới vào Response hoặc thêm một Optional Parameter vào Request **không** phải là Breaking Change.

## 2. Quy trình Deprecation (Khai tử)

Khi bắt buộc phải có Breaking Changes, ta cần làm theo quy trình:

### Bước 1: Giao tiếp & Thông báo (Communication)
- Thông báo cho các Client/Partner qua Email, Slack, Developer Portal về lộ trình.
- Cập nhật Changelog / Release Notes.
- Cung cấp rõ tài liệu: API nào sẽ thay thế API cũ, cách chuyển đổi (Migration Guide).

### Bước 2: Thiết lập thời gian chuyển giao (Sunset Period)
- Tuyệt đối không xóa API cũ ngay lập tức.
- Thường cung cấp từ **3 đến 6 tháng** (hoặc chí ít là 1 tháng đối với API nội bộ) để Client kịp nâng cấp.
- Giai đoạn này gọi là "Sunset Period". API cũ vẫn hoạt động 100% nhưng được đánh dấu là *Deprecated*.

### Bước 3: Sử dụng Standard HTTP Headers
Khi Client gọi vào API đã bị Deprecate, Backend trả về kèm theo các Headers theo chuẩn IETF:
- `Deprecation`: Ngày/Giờ mà API bắt đầu bị đánh dấu không còn khuyên dùng (ví dụ: `Fri, 01 May 2026 23:59:59 GMT`).
- `Sunset`: Ngày/Giờ chính thức hệ thống sẽ vô hiệu hóa (tắt) API này.
- `Link`: Header trỏ tới Endpoint mới để thay thế.

Ví dụ:
```http
HTTP/1.1 200 OK
Deprecation: Fri, 01 May 2026 23:59:59 GMT
Sunset: Mon, 01 Jan 2027 23:59:59 GMT
Link: </api/v2/users/123>; rel="alternate"
```

### Bước 4: Monitoring (Giám sát)
- Backend lưu Log các request gọi vào API bị Deprecate (lưu IP, API Key, User-Agent...).
- Khi đến sát ngày "Sunset", kiểm tra xem ai vẫn còn gọi và chủ động gửi email cảnh báo lần cuối.

### Bước 5: Thực thi Sunset (Blackout test)
- Vài tuần trước ngày Sunset chính thức, có thể áp dụng chiến lược "Brownout" (Tạm thời trả về lỗi 410 Gone hoặc 503 Service Unavailable trong vài giờ) để ép các Client lười biếng phải nâng cấp.
- Ngày Sunset: Chính thức xóa bỏ code, trả về `410 Gone` vĩnh viễn (Không nên trả 404 Not Found vì 410 chỉ rõ rằng resource này từng tồn tại nhưng đã bị xóa theo chủ ý).

## 3. Demo Code

Vui lòng chạy file `demo_deprecation.py` và gọi các API sau để thấy trực quan cách chúng hoạt động:
1. `GET /api/v1/users/1` (API cũ - Xem tab Headers trên Postman sẽ thấy cảnh báo).
2. `GET /api/v2/users/1` (API mới - Hoạt động bình thường).
