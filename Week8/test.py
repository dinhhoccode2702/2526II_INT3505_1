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
        payload = {"name": "Dinh Nguyen", "email": "dinh@uet.vnu.edu.vn"}
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

if __name__ == '__main__':
    unittest.main()