# Kế Hoạch Nâng Cấp API (API Migration Plan)

Bản kế hoạch này cung cấp lộ trình chuẩn mực để nâng cấp API từ phiên bản cũ (v1) lên phiên bản mới (v2) đảm bảo nguyên tắc **Zero Downtime** và không làm gián đoạn trải nghiệm của người dùng/client.

## 1. Giai đoạn 1: Chuẩn bị & Thiết kế (Planning & Design)
- **Đánh giá phạm vi thay đổi:** Xác định những trường dữ liệu nào bị thay đổi kiểu, bị xóa hoặc cấu trúc JSON nào bị điều chỉnh.
- **Thiết kế v2:** Xây dựng tài liệu đặc tả (ví dụ: OpenAPI/Swagger) cho phiên bản v2.
- **Chiến lược Adapter (DTO):** Cấu trúc lại code ở Backend sao cho v1 và v2 dùng chung Database/Core Logic nhưng trả về dữ liệu qua các Adapter khác nhau để tránh lặp code.

## 2. Giai đoạn 2: Phát triển & Triển khai song song (Concurrent Release)
- Phát triển API v2 song song với v1. 
- API v1 vẫn giữ nguyên hoàn toàn logic hiện tại để không gây ảnh hưởng.
- Deploy API v2 lên môi trường Production. Lúc này cả `/api/v1/...` và `/api/v2/...` đều hoạt động đồng thời.

## 3. Giai đoạn 3: Giao tiếp & Công bố (Communication & Deprecation)
- **Migration Guide:** Tạo tài liệu hướng dẫn chuyển đổi từ v1 sang v2. Nêu rõ lợi ích khi chuyển sang v2 và code mẫu (snippets).
- **Deprecation Headers:** Bổ sung các Headers vào API v1 để cảnh báo Client:
  - `Deprecation: <Ngày>`
  - `Sunset: <Ngày khai tử>`
  - `Link: </api/v2/...>; rel="alternate"`
- Gửi Email / Thông báo trên Developer Portal cho các đối tác đang sử dụng v1.

## 4. Giai đoạn 4: Thời gian chuyển giao (Sunset Period)
- Duy trì cả 2 phiên bản trong một khoảng thời gian (thường từ **3 đến 6 tháng** đối với API public).
- **Monitoring:** Sử dụng các công cụ Monitor (như Datadog, ELK, CloudWatch) để theo dõi lưu lượng request gọi vào API v1. Gửi email trực tiếp đến những user vẫn đang tích cực dùng v1 khi sắp đến deadline.

## 5. Giai đoạn 5: Cảnh báo "Mất điện" (Brownouts)
- 1-2 tuần trước ngày khai tử chính thức, thực hiện các đợt "Brownout".
- Brownout là việc cố tình làm API v1 trả về lỗi (ví dụ `503 Service Unavailable` hoặc `429 Too Many Requests`) trong các khung giờ ngắn (15-30 phút).
- Mục đích: "Đánh thức" những client/hệ thống đã phớt lờ cảnh báo email, buộc họ phải khẩn trương nâng cấp.

## 6. Giai đoạn 6: Khai tử chính thức (Sunset / End of Life)
- Sau khi thời gian Sunset kết thúc, xóa code API v1 (hoặc vô hiệu hóa router).
- Thay vì trả về `404 Not Found`, hãy cài đặt để API v1 trả về `410 Gone`. HTTP Status này chỉ ra rõ ràng rằng resource này từng tồn tại nhưng đã bị gỡ bỏ có chủ ý.
- Xóa các Adapter của v1 để làm sạch codebase. Hoàn thành quá trình nâng cấp!
