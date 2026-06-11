"""
database.py - Quản lý tất cả các hoạt động cơ sở dữ liệu SQLite
"""
import os
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_FILE = Path(os.getenv('DB_FILE', '/tmp/store.db' if os.getenv('VERCEL') else Path(__file__).with_name('store.db')))


def get_connection():
    """Trả về kết nối SQLite"""
    return sqlite3.connect(DB_FILE)


def init_db():
    """Khởi tạo các bảng cơ sở dữ liệu nếu chưa tồn tại"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Bảng người dùng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Bảng sản phẩm
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                image_url TEXT,
                description TEXT,
                stock INTEGER DEFAULT 0
            )
        ''')
        
        # 3. Bảng đơn hàng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
    
    print("[HỆ THỐNG]: Đã khởi tạo cấu trúc Database SQLite thành công!")


# ========== NGƯỜI DÙNG ==========

def user_exists(email: str) -> bool:
    """Kiểm tra email có tồn tại không"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        return cursor.fetchone() is not None


def create_user(fullname: str, email: str, password: str) -> bool:
    """Tạo người dùng mới"""
    try:
        hashed_password = generate_password_hash(password)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)',
                (fullname, email, hashed_password)
            )
            conn.commit()
        return True
    except Exception as e:
        print(f"[LỖI TẠO NGƯỜI DÙNG]: {e}")
        return False


def get_user_by_email(email: str) -> tuple:
    """Lấy thông tin người dùng theo email"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT fullname, email, password FROM users WHERE email = ?', (email,))
        return cursor.fetchone()


def update_user_password(email: str, new_password: str) -> bool:
    """Cập nhật mật khẩu người dùng"""
    try:
        hashed_password = generate_password_hash(new_password)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"[LỖI CẬP NHẬT MẬT KHẨU]: {e}")
        return False
