# Đặt tên database làm một biến để dùng chung
import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
db_name = "shopee_order.db"

def connecting():
    return sqlite3.connect(db_name)

def table_shopee_profit():
    try:
        # Dùng biến DB_NAME ở đây
        with sqlite3.connect(db_name) as connect:
            cursor = connect.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ordering(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT UNIQUE NOT NULL,
                    sku_id TEXT NOT NULL,
                    sku_name TEXT,
                    channel TEXT NOT NULL,
                    revenue REAL NOT NULL,
                    platform_fee REAL NOT NULL,
                    shipping_gap REAL DEFAULT 0,
                    cogs REAL NOT NULL,
                    order_date TEXT NOT NULL,
                    customer_name TEXT
                )
            """)
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if connect:
            connect.close()
            print("Đã đóng kết nối an toàn.")

def insert_order(ordering_list):
    try:
        with sqlite3.connect(db_name) as connect:
            c = connect.cursor()
            c.execute("""
            INSERT INTO ordering (order_id, sku_id, sku_name, channel, revenue, platform_fee, shipping_gap, cogs, order_date)
                       VALUES (?,?,?,?,?,?,?,?,?)
                     """,ordering_list)
        return True
    except sqlite3.IntegrityError:
        print("lỗi trùng lặp")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if connect:
            connect.close()
            print("Đã đóng kết nối an toàn")

            

    





