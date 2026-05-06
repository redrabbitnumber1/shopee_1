# Đặt tên database làm một biến để dùng chung
import sys
sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
db_name = "shopee_order.db"

def connecting():
    return sqlite3.connect(db_name)

def setup():
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



#connect là lệnh để nối với database
#cursor là để kết nối execute với database
# execute là lệnh thực thi

def query_profit_by_channel():
    connect = None
    try:
        with sqlite3.connect(db_name) as connect:
            c =connect.cursor()
            c.execute(""" SELECT channel, 
                      COUNT(*), SUM(revenue), 
                      SUM(platform_fee+shipping_gap), 
                      SUM(cogs),
                      SUM(revenue - platform_fee - shipping_gap - cogs) as profit,
                      ROUND(SUM(revenue - platform_fee - shipping_gap - cogs) * 100.0 / SUM(revenue), 1) 
                      FROM ordering
                      GROUP BY channel
                      ORDER BY profit DESC
""")
            #dòng ở trước FROM không có dấu phẩy
        a =  c.fetchall()
        return a
    except Exception as i:
        print(f"Lỗi tại {i} ")
    finally:
        if connect:
            connect.close()
            print("Đã đóng kết nối an toàn")

def query_profit_by_sku():
    connect = None
    try:
        with sqlite3.connect(db_name) as connect:
            c = connect.cursor()
            c.execute(""" SELECT sku_id, sku_name, 
                      COUNT(*),
                      SUM(revenue - platform_fee - shipping_gap - cogs) as profit,
                      ROUND(SUM(revenue - platform_fee - shipping_gap - cogs) * 100.0 / SUM(revenue), 1) 
                      FROM ordering
                      GROUP BY sku_id, sku_name
                      ORDER BY profit ASC
""")
            result = c.fetchall()
            return result
    except Exception as i:
        print("Error at i")
    finally:
        if connect:
            connect.close()
            print(" Đã ngắt kết nối thành công")

def query_profit_by_month():
    connect = None
    try:
        with sqlite3.connect(db_name) as connect:
            c =connect.cursor()
            c.execute("""SELECT SUBSTR(order_date, 1, 7) as month,
                      COUNT(*),
                      SUM(revenue),
                      SUM(revenue - platform_fee - shipping_gap - cogs) as profit
                      FROM ordering
                      GROUP BY month
                      ORDER by month
""")
            result = c.fetchall()
            return result
    except Exception as e:
        print(f"Error as {e}")
    finally:
        connect.close()
        print("Ngắt kết nối thành công")

def query_total_summary():
    connect = None # nếu như lệnh try bị lỗi
    try:
        with sqlite3.connect(db_name) as connect:
            c = connect.cursor()
            c.execute(""" SELECT COUNT(*),
                      COUNT( DISTINCT sku_id),
                      COUNT (DISTINCT channel),
                      SUM(revenue),
                      SUM(revenue - platform_fee - shipping_gap - cogs) as profit
                      FROM ordering
""")
        result = c.fetchall()
        return result
    except Exception as i:
        print(f"Error as {i}")
    finally:
        connect.close()
        print("Ngắt kết nối thành công")

query_total_summary()
print("Test 4: query_total_summary()")

row = query_total_summary()
# khi một fetchall được tạo ra, nó chỉ có len = 1 do nó là một list(tuple) list bao tuple
# chỉ có tuple mới có nhiều giá trị khác nhau còn list thì chỉ có 1,\
#nên khi yêu cầu chia nhiều dữ liệu thì sẽ sai
tong_don, so_sku, so_channel, tong_dt, tong_profit = row[0]
# khi làm như row[0], chính là nói rằng, hãy truy cập dữ liệu thứ nhất là tuple có nhiều giá trị thì sẽ hết lỗi

print(f"  Tổng đơn: {tong_don}")
print(f"  Số SKU: {so_sku}")
print(f"  Số channel: {so_channel}")
print(f"  Tổng DT: {tong_dt:,.0f}đ")
print(f"  Tổng profit: {tong_profit:,.0f}đ")

