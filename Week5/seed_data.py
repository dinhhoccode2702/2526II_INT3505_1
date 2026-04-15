import pymysql
import time

DB_CONFIG = {
    "host": "localhost",
    "user": "root",       # Điền user MySQL của bạn
    "password": "Dinh2722005@", # Điền pass MySQL của bạn
}

def seed():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 1. Tạo Database và Bảng
    cursor.execute("CREATE DATABASE IF NOT EXISTS book_manager")
    cursor.execute("USE book_manager")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            available BOOLEAN DEFAULT TRUE,
            INDEX idx_id (id)  
        )
    """)
    
    # 2. Xóa dữ liệu cũ nếu có và bắt đầu chèn 1M bản ghi
    cursor.execute("TRUNCATE TABLE books")
    print("Bắt đầu chèn 1,000,000 bản ghi. Vui lòng đợi 1-2 phút...")
    
    batch_size = 10000
    
    for i in range(100): # 100 * 10,000 = 1,000,000
        records = [(f"Book Title {i*batch_size + j}", f"Author {i*batch_size + j}", True) for j in range(1, batch_size + 1)]
        cursor.executemany("INSERT INTO books (title, author, available) VALUES (%s, %s, %s)", records)
        conn.commit()
        print(f"Đã chèn {(i+1) * batch_size} bản ghi...")

    conn.close()

if __name__ == "__main__":
    seed()