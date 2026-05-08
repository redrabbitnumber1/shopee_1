from set_up import setup, insert_order
from analyzer import show_summary, show_by_channel, show_by_sku, show_by_month
from importer import import_from_csv
from datetime import date
import sqlite3


db_name = "shopee_order.db"


def menu_them_order(order_id, sku_id, sku_name, channel, revenue, platform_fee, shipping_gap, cogs):
    connect = None
    today = date.today().strftime("%Y-%m-%d")

    
    try:
        # order_id =input("order_id là: ").strip().upper()
        # sku_id =input("sku_id, mã sản phẩm là: ").strip().upper()
        # sku_name = input("tên sản phẩm là: ").strip()
        # channel = input("Tên kênh").strip()
        # revenue =int(input("Doanh thu: "))
        # platform_fee = int(input("Phí sàn thương mại: "))
        # shipping_gap = int(input("Phí ship: "))
        # cogs = int(input("giá vốn: "))
        profit = revenue - platform_fee - shipping_gap - cogs
        if revenue > 0:
              margin = profit * 100.0 / revenue
              print(f"""Profit = {profit}
                    - Margin = {margin}
                    - Preview hiển thị
                    - Confirm lưu
                    - Insert thành công""")

        else:
                print(f"Bị lỗ {profit}")
        
        with sqlite3.connect(db_name) as connect:
            c = connect.cursor()
            confirm = input("Bạn có đồng ý lưu dữ liệu (y/n)").strip().lower()
            if confirm == "y":
             c.execute("""INSERT INTO ordering (order_id, sku_id, sku_name, channel, revenue, platform_fee, shipping_gap, cogs, order_date)
                      VALUES (?,?,?,?,?,?,?,?,?)
""",(order_id, sku_id, sku_name, channel, revenue, platform_fee, shipping_gap, cogs, today))

            return True
    except Exception as i:
        print(f"Lỗi tại {i}")
    finally:
        if connect:
            connect.close()
            print("Đã đóng kết nối an toàn")
            

def menu_import_csv(filepath, sku_id, sku_name, cogs):
    import_from_csv()
    imported, skipped = import_from_csv()
    print(f"  ✓ Import xong: {imported} đơn mới, {skipped} bỏ qua")


def main():
    setup()
    print("\n" + "="*52)
    print("   SHOPEE PROFIT TRACKER — InsightSME v0.1")
    print("="*52)
    
    while True:
        print(""""\n  1. Xem tổng quan"
     "  2. Báo cáo theo channel"
     "  3. Báo cáo theo SKU"
     "  4. Báo cáo theo tháng"
     "  5. Thêm order thủ công"
     "  6. Import CSV từ Shopee"
     "  0. Thoát"
""")
        choice = input("Lựa chọn của bạn là: ")
        if choice == "1":
            show_summary()
        elif choice == "2":
            show_by_channel()
        elif choice =="3":
            show_by_sku()
        elif choice == "4":
            show_by_month()
        elif choice == "5":
            menu_them_order()
        elif choice == "6":
            menu_import_csv()
        elif choice == "0":
            break
        else:
            print("hãy chọn từ 1 đến 6")
            
    
