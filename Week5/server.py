from flask import Flask, jsonify, request
import pymysql
import time

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",       # Điền user MySQL của bạn
    "password": "Dinh2722005@", # Điền pass MySQL của bạn
    "database": "book_manager",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/api/books', methods=['GET'])
def get_books():
    """1. Phân trang LIMIT / OFFSET truyền thống"""
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Bắt đầu bấm giờ chạy Query
    start_time = time.time()
    
    cursor.execute("SELECT * FROM books ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
    data = cursor.fetchall()
    
    # Kết thúc bấm giờ
    query_time_ms = (time.time() - start_time) * 1000 
    
    conn.close()
    
    return jsonify({
        "strategy": "offset",
        "offset": offset,
        "limit": limit,
        "query_time_ms": round(query_time_ms, 2), # Thời gian chạy tính bằng mili-giây
        "data": data
    }), 200

@app.route('/api/books/cursor', methods=['GET'])
def get_books_cursor():
    """1b. Phân trang CURSOR dựa trên ID"""
    cursor_id = request.args.get('cursor', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)
    
    conn = get_db_connection()
    db_cursor = conn.cursor()
    
    # Bắt đầu bấm giờ chạy Query
    start_time = time.time()
    
    # WHERE id > cursor_id sử dụng B-Tree Index, bỏ qua hoàn toàn các bản ghi đằng trước
    db_cursor.execute("SELECT * FROM books WHERE id > %s ORDER BY id ASC LIMIT %s", (cursor_id, limit))
    data = db_cursor.fetchall()
    
    # Kết thúc bấm giờ
    query_time_ms = (time.time() - start_time) * 1000
    
    conn.close()
    
    next_cursor = data[-1]["id"] if data else None
    
    return jsonify({
        "strategy": "cursor",
        "next_cursor": next_cursor,
        "limit": limit,
        "query_time_ms": round(query_time_ms, 2), # Thời gian chạy tính bằng mili-giây
        "data": data
    }), 200

@app.route('/api/books/page', methods=['GET'])
def get_books_page():
    """1c. Phân trang kiểu Page-based (Dùng số trang)"""
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    
    if page < 1:
        page = 1
        
    # Tự động quy đổi từ page ra offset
    offset = (page - 1) * limit
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Bắt đầu bấm giờ
    start_time = time.time()
    
    # 1. Lấy dữ liệu sách
    cursor.execute("SELECT * FROM books ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
    data = cursor.fetchall()
    
    # 2. Đếm tổng số bản ghi để phục vụ giao diện (Bắt buộc với Page-based đích thực)
    # cursor.execute("SELECT COUNT(id) as total FROM books")
    # total_items = cursor.fetchone()['total']
    # total_pages = (total_items + limit - 1) // limit
    
    # Kết thúc bấm giờ (tính cả thời gian Get Data + Count Data)
    query_time_ms = (time.time() - start_time) * 1000
    
    conn.close()
    
    return jsonify({
        "strategy": "page-based",
        "page": page,
        "limit": limit,
        # "total_items": total_items,
        # "total_pages": total_pages,
        "query_time_ms": round(query_time_ms, 2), # Thời gian chạy tính bằng mili-giây
        "data": data
    }), 200

if __name__ == '__main__':
    app.run(debug=True)