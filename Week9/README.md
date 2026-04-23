# API Versioning: Mô hình Dùng chung Database & Design Pattern "Adapter"

Tài liệu này giải thích cách hoạt động của hệ thống API Versioning được triển khai trong dự án, đặc biệt tập trung vào vấn đề chia sẻ **Cơ Sở Dữ Liệu (Database)** giữa các phiên bản.

## Vấn đề đặt ra

Khi nâng cấp API (từ `v1` lên `v2`), nếu ta nhân bản (copy) toàn bộ source code cũ và viết lại logic database, dự án sẽ nhanh chóng phình to và gặp tình trạng "nợ kỹ thuật" (Tech Debt). 
Ví dụ: Khi sửa một câu truy vấn trong DB, ta phải sửa cả ở code v1 và code v2.

## Giải pháp: Pattern "Adapter" (hay DTO - Data Transfer Object)

Thay vì tách biệt hoàn toàn từ đầu đến cuối, cả **API v1** và **API v2** đều:
1. **Dùng chung** các hàm truy vấn CSDL (Core DB/Services).
2. **Khác biệt** ở khâu "Đóng gói dữ liệu trả về" (Response Mapping). 

Để làm được điều này, ta dùng các hàm **Adapter**.

### Cách hoạt động:
1. Client gửi Request lên Server (có thể qua `/api/v1/products` hoặc Header `Accept-Version: 2`).
2. Controller nhận Request và gọi hàm truy vấn Database chung (`get_all_products_from_db`).
3. Dữ liệu từ DB (đầy đủ các trường) được truyền vào lớp **Adapter** tương ứng:
   - Nếu là **v1**: `adapter_v1` sẽ nhận dữ liệu DB, **cắt bỏ** đi giá và số lượng tồn kho, trả về một Object đơn giản (chỉ chứa `id`, `name`).
   - Nếu là **v2**: `adapter_v2` sẽ nhận dữ liệu DB, **chuyển đổi** tên field (ví dụ: `name` -> `product_name`) và bổ sung các logic mới như tính toán trạng thái `is_available` dựa trên lượng tồn kho.
4. Controller gói dữ liệu đã qua Adapter vào JSON và trả về cho Client.

### Lợi ích của thiết kế này:

- **Giữ cho Business Logic duy nhất (Single Source of Truth):** Logic tính toán tổng tiền, kiểm tra tồn kho, lấy dữ liệu DB chỉ nằm ở một chỗ.
- **Tránh rò rỉ dữ liệu (Data Leakage):** Không trả thẳng kết quả DB (`SELECT *`) ra ngoài API. Nếu DB thêm cột `password` hay `secret_key`, các phiên bản API cũ không vô tình làm rò rỉ vì Adapter đã giới hạn chính xác những trường nào được phép đẩy ra.
- **Dễ dàng loại bỏ (Deprecate):** Khi không ai dùng V1 nữa, bạn chỉ việc xóa Route `/v1` và hàm `adapter_v1`. Toàn bộ hệ thống core (Database, V2) không bị ảnh hưởng.

### Tóm tắt luồng hoạt động
`Client --> Controller (v1 hoặc v2) --> Shared DB Model --> DB Data --> Adapter (v1 hoặc v2) --> Controller --> JSON Response`
