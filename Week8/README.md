# HƯỚNG DẪN KIỂM THỬ API TỰ ĐỘNG VÀ HIỆU NĂNG (UET ASSIGNMENT)

Tài liệu này cung cấp lộ trình từ cài đặt, viết mã nguồn đến thực thi kiểm thử tự động và đo lường hiệu năng cho hệ thống API Flask.

---

## 🎯 MỤC TIÊU CẦN ĐẠT
1. **Các loại test:** Hiểu và áp dụng Unit Test, Integration Test, Performance Test.
2. **Công cụ:** Sử dụng thành thạo Postman, Newman, và k6.
3. **Kỹ năng thiết yếu:**
   - Viết bộ test tự động cho các endpoint.
   - Đo lường và đánh giá hiệu năng API (Response Time, Error Rate).
4. **Thực hành:**
   - Tạo Test Suite trong Postman cho ít nhất 5 endpoints.
   - Chạy test tự động bằng Newman để xuất báo cáo.

---

## I. KIẾN THỨC NỀN TẢNG (THE TESTING PYRAMID)

1. **Unit Test (Kiểm thử đơn vị):** Kiểm tra các hàm logic riêng lẻ (ví dụ: hàm tính tổng tiền giỏ hàng). Thường dùng thư viện `unittest` hoặc `pytest` trong Python.
2. **Integration Test (Kiểm thử tích hợp):** Kiểm tra sự phối hợp giữa API và Database hoặc luồng chạy giữa các API. Đảm bảo dữ liệu gửi lên được lưu đúng và truy xuất được.
3. **Performance Test (Kiểm thử hiệu năng):** Đo lường tốc độ (`Response Time`) và sức chịu tải (`Error Rate`) của hệ thống khi có nhiều người dùng cùng lúc bằng cách tạo ra các người dùng ảo (VU).

---

## II. CÀI ĐẶT MÔI TRƯỜNG (PREREQUISITES)

Mở **PowerShell (Run as Administrator)** và thực hiện các lệnh sau:

### 1. Cài đặt Newman (Chạy Postman bằng dòng lệnh)

```powershell
# Cài đặt Newman global
npm install -g newman

# Cài đặt công cụ xuất báo cáo HTML chuyên nghiệp
npm install -g newman-reporter-htmlextra
```

### 2. Cài đặt k6 (Công cụ Load Test chuyên nghiệp)
- Tải file `.msi` tại: [k6 Releases](https://github.com/grafana/k6/releases)
- Hoặc nếu dùng Chocolatey (Windows): `choco install k6`
- Kiểm tra cài đặt thành công: `k6 version`

---

## III. MÃ NGUỒN SERVER DEMO (`app.py`)
Lưu đoạn code sau vào file `app.py` và chạy lệnh `python app.py` để bật Server.

```python
from flask import Flask, request, jsonify
import time

app = Flask(__name__)
users_db = {}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": time.time()}), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing data"}), 400
    user_id = str(data['user_id'])
    if user_id in users_db:
        return jsonify({"error": "User already exists"}), 409
    users_db[user_id] = data
    return jsonify(data), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(str(user_id))
    if not user:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(user), 200

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    items = data.get('items', [])
    total = sum(item['price'] * item['quantity'] for item in items)
    if total > 5000:
        return jsonify({"error": "Limit exceeded", "total": total}), 403
    return jsonify({"status": "success", "total": total}), 200

@app.route('/api/heavy-calculation', methods=['GET'])
def heavy():
    n = int(request.args.get('n', 1000))
    result = sum(i * i for i in range(n))
    return jsonify({"result": result}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## IV. KIỂM THỬ TỰ ĐỘNG VỚI POSTMAN & NEWMAN

### 1. Kỹ thuật Scripting trong Postman
- **Pre-request Script (Request POST):** Dùng để tạo dữ liệu ngẫu nhiên, tránh trùng lặp khi test tải tự động.
  ```javascript
  var randomId = Math.floor(Math.random() * 1000000);
  pm.variables.set("dynamic_user_id", randomId);
  ```

- **Tests Script (Request GET):** Kiểm tra kết quả trả về bằng Assertions.
  ```javascript
  pm.test("Status code là 200", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Thời gian phản hồi < 200ms", function () {
      pm.expect(pm.response.responseTime).to.be.below(200);
  });
  ```

### 2. Chạy tự động bằng Newman
Sau khi cài đặt môi trường và xuất Collection (`Local_Test.json`) từ Postman, mở Terminal tại thư mục chứa file test và chạy lệnh:

```powershell
npx newman run Local_Test.json -r cli,htmlextra --reporter-htmlextra-export report.html
```
*(Thêm `-e Env.json` vào lệnh trên nếu bạn sử dụng file JSON chứa biến môi trường).*

**Mở file `report.html` vừa được văng ra để xem báo cáo chi tiết sự chuyên nghiệp của Automation Test.**

---

## V. ĐO HIỆU NĂNG VỚI k6

Tạo file `load_test.js`:

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 20 }, // Giai đoạn 1: Tăng dần lên 20 người dùng ảo
    { duration: '20s', target: 20 }, // Giai đoạn 2: Duy trì ép tải ở mức 20 VU
    { duration: '10s', target: 0 },  // Giai đoạn 3: Giảm dần và kết thúc
  ],
};

export default function () {
  let res = http.get('http://127.0.0.1:5000/api/heavy-calculation?n=5000');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

**Lệnh thực thi ép sức chịu tải Server:**
```powershell
k6 run load_test.js
```

**📊 Các chỉ số vàng hiệu năng cần nhớ:**
- `http_req_duration (avg, p95)`: Thời gian phản hồi. `p(95)` là con số vàng biểu thị 95% request có thời gian xử lý nhanh hơn mốc này. (Kỳ vọng: `< 200ms`)
- `http_req_failed`: Tỉ lệ lỗi. (Mục tiêu bắt buộc với API chuẩn: `0.00%`)
- `iterations`: Tổng số request API đã xử lý được trong suốt quá trình.

---

## VI. CÁC LỖI THƯỜNG GẶP (CẨM NANG TROUBLESHOOTING)

| Cảnh báo lỗi | Nguyên nhân | Hướng giải quyết |
|---|---|---|
| **404 Not Found** | URL sai thông số hoặc biến `{{id}}` chưa được nạp dữ liệu. | Kiểm tra biến trên tab Environment (Postman) hoặc chèn cờ chỉ định file `-e` trong lệnh Newman. |
| **415 Unsupported Media Type** | Gửi Body Request dạng JSON nhưng thiếu header `Content-Type`. | Trong Postman: Tab Body -> chọn kiểu `raw` -> Đổi Text thành `JSON` ở menu nhỏ. |
| **Failure % cao / Mã 409 Conflict** | Trùng `user_id` khi ép nhiều lệnh tạo mới vào Database. | Sử dụng biến sinh lập trình tự động bằng khối mã "Pre-request Script" (như ở mục IV). |
| **Lệnh "newman" không nhận dạng được** | Lỗi thư mục hệ thống chưa tìm đến thư viện Node.js toàn cục. | Thay bằng cụm tiền tố chạy trực tiếp: `npx newman ...` trên shell. |

---
*Dự án thực hành chuyên ngành - Đóng góp nội dung tổng hợp từ khóa:* **Nguyễn Ngọc Dinh (23020021)**
