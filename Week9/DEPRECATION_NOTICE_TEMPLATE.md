# Mẫu Thông Báo Deprecation Cho Developers (Email / Slack)

Giao tiếp rõ ràng là chìa khóa để việc nâng cấp API diễn ra suôn sẻ. Dưới đây là mẫu (template) chuẩn bạn có thể dùng để gửi email hoặc đăng lên kênh Slack cộng đồng cho các Developer.

---

## 📧 Email Template: Thông báo khai tử API v1

**Tiêu đề (Subject):** [Action Required] Deprecation Notice: Nâng cấp lên API v2 trước ngày 01/01/2027

**Nội dung (Body):**

Chào bạn (Dear Developer),

Tại [Tên Công Ty/Sản Phẩm], chúng tôi không ngừng cải thiện hệ thống để mang lại hiệu năng và trải nghiệm tốt nhất. Hôm nay, chúng tôi xin thông báo về việc ra mắt **API v2** và lộ trình **khai tử (Deprecation)** đối với **API v1**.

### 1. Chuyện gì đang xảy ra?
Kể từ hôm nay, toàn bộ các endpoints thuộc nhóm `https://api.domain.com/v1/*` đã chính thức chuyển sang trạng thái **Deprecated** (Không còn khuyên dùng).
Chúng tôi đã ra mắt hệ thống `v2` thay thế với nhiều cải tiến:
- Tối ưu hóa tốc độ truy vấn (nhanh hơn 30%).
- Cấu trúc dữ liệu JSON được chuẩn hóa (Tham khảo sự thay đổi tại `first_name`, `last_name`).

### 2. Thời gian bạn cần lưu ý (Timeline)
- **Hôm nay:** API v1 bắt đầu bị đánh dấu Deprecated. Nó vẫn hoạt động bình thường, nhưng bạn không nên tích hợp thêm tính năng mới vào hệ thống này.
- **Ngày 01/12/2026 (Brownout):** Chúng tôi sẽ tiến hành ngắt kết nối ngẫu nhiên 15 phút mỗi ngày đối với v1 để giả lập lỗi và cảnh báo.
- **Ngày 01/01/2027 (Sunset):** API v1 sẽ chính thức bị **KHAI TỬ**. Bất kỳ truy vấn nào gọi vào v1 sẽ nhận được lỗi `410 Gone`.

### 3. Bạn cần làm gì? (Call to Action)
Vui lòng lên kế hoạch di chuyển (migrate) code của bạn sang API v2 **trước ngày 01/01/2027** để đảm bảo ứng dụng của bạn không bị gián đoạn.
👉 Xem tài liệu hướng dẫn chuyển đổi chi tiết tại đây: [Link tới Migration Guide]

### 4. Cần hỗ trợ?
Nếu bạn gặp khó khăn trong quá trình chuyển đổi, hãy reply lại email này hoặc liên hệ với đội ngũ hỗ trợ qua kênh Slack `#api-support`.

Cảm ơn bạn đã luôn đồng hành!

Trân trọng,
**[Tên Đội Ngũ Kỹ Thuật]**
---

## 💡 Lưu ý khi gửi:
1. Luôn đính kèm link tới tài liệu **Migration Guide** (chỉ rõ code cũ trông thế nào, code mới thay đổi ra sao).
2. Gửi nhắc nhở (Reminder) ở các mốc: Trước 3 tháng, 1 tháng và 1 tuần trước ngày Sunset.
