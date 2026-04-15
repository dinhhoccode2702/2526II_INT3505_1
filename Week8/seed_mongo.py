from mongoengine import connect, Document, StringField, IntField, errors
import sys

# 1. Kết nối đến DB
# Thêm alias và timeout để script không bị treo nếu không thấy Database
try:
    connect(
        db="Test",
        host="mongodb://localhost:27017/Test",
        serverSelectionTimeoutMS=2000 
    )
    print("--- Kết nối MongoDB thành công ---")
except Exception as e:
    print(f"Lỗi kết nối: {e}")
    sys.exit(1)

# 2. Khai báo Schema
class User(Document):
    user_id = IntField(required=True, unique=True)
    name = StringField(required=True)
    email = StringField(required=True)
    
    meta = {'collection': 'users'}

def seed_data():
    print("Đang làm sạch collection 'users'...")
    # Xóa dữ liệu cũ để tránh lỗi 'unique=True' khi chạy lại nhiều lần
    User.objects().delete() 
    
    users_data = [
        {"user_id": 1, "name": "Nguyen Van A", "email": "nva@gmail.com"},
        {"user_id": 2, "name": "Tran Thi B", "email": "ttb@gmail.com"},
        {"user_id": 3, "name": "Le Van C", "email": "lvc@gmail.com"},
        {"user_id": 4, "name": "Hoang Van D", "email": "hvd@gmail.com"},
        {"user_id": 5, "name": "Phan Thi E", "email": "pte@gmail.com"}
    ]
    
    print("Đang nạp dữ liệu mới...")
    count = 0
    for u_data in users_data:
        try:
            user = User(**u_data)
            user.save()
            print(f" [+] Đã thêm: {u_data['name']}")
            count += 1
        except errors.NotUniqueError:
            print(f" [!] Bỏ qua: {u_data['user_id']} đã tồn tại.")
        except Exception as e:
            print(f" [X] Lỗi khi thêm {u_data['name']}: {e}")
            
    print(f"\nHoàn thành! Đã nạp thành công {count}/{len(users_data)} users.")

if __name__ == "__main__":
    seed_data()