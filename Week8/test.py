import unittest
import json
import mongomock
from mongoengine import connect, disconnect
from app import app, User # Giả sử bạn đã chuyển Class User vào file app.py

class TestUserAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 1. Ngắt kết nối thật để tránh ghi đè dữ liệu thật
        disconnect()
        # 2. Kết nối tới Mongomock (DB ảo trên RAM)
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

    def setUp(self):
        self.app = app.test_client()
        # Xóa sạch dữ liệu trong DB ảo trước mỗi bài test
        User.objects.delete()

    # --- TEST 1: Tạo User thành công ---
    def test_create_user_db(self):
        # 1. Định nghĩa dữ liệu đầu vào
        payload = {"name": "Dinh Nguyen", "email": "dinh@uet.vnu.edu.vn"}
        # 2. Gọi API POST
        response = self.app.post('/api/users', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        # Kiểm tra trực tiếp trong DB ảo xem dữ liệu đã nằm đó chưa
        user_in_db = User.objects(email="dinh@uet.vnu.edu.vn").first()
        self.assertIsNotNone(user_in_db)
        self.assertEqual(user_in_db.name, "Dinh Nguyen")

    # --- TEST 2: Lấy User đã tồn tại ---
    def test_get_user_success(self):
        # Tạo sẵn một user "mồi" trong DB ảo
        temp_user = User(user_id=10, name="Hoàng Bỏn", email="bon@gmail.com").save()
        
        # Gọi API để lấy user đó
        response = self.app.get(f'/api/users/10')
        data = json.dumps(response.get_json(), ensure_ascii=False)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hoàng Bỏn", data)
    # --- TEST 3: Tạo User thất bại (Thiếu thông tin) ---
    def test_create_user_missing_field(self):
        # 1. Arrange: Dữ liệu thiếu trường 'email'
        payload = {"name": "User Loi"} 
        
        # 2. Act: Gửi request
        response = self.app.post('/api/users', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        # 3. Assert: Phải trả về lỗi 400
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    # --- TEST 4: Checkout thành công (Dưới hạn mức) ---
    def test_checkout_success(self):
        # 1. Arrange: Giỏ hàng tổng 1000 + 2000 = 3000 ( < 5000 )
        payload = {
            "items": [
                {"price": 500, "quantity": 2},
                {"price": 2000, "quantity": 1}
            ]
        }
        
        # 2. Act
        response = self.app.post('/api/cart/checkout', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        # 3. Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')
        self.assertEqual(response.get_json()['total_paid'], 3000)

    # --- TEST 5: Checkout thất bại (Vượt hạn mức 5000) ---
    def test_checkout_over_limit(self):
        # 1. Arrange: Giỏ hàng tổng 6000 ( > 5000 )
        payload = {
            "items": [
                {"price": 3000, "quantity": 2}
            ]
        }
        
        # 2. Act
        response = self.app.post('/api/cart/checkout', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        # 3. Assert: Phải trả về lỗi 403 Forbidden
        self.assertEqual(response.status_code, 403)
        self.assertIn("Vượt quá hạn mức", response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()