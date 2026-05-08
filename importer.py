import sqlite3
import csv
from set_up import insert_order, setup
from datetime import date

def  _parse_shopee_number(number):
    if not number or str(number).strip() == "":
        return 0.0
    
    # Xử lý: Xóa dấu chấm (phân cách hàng nghìn) và đổi dấu phẩy (thập phân) thành dấu chấm
    # Giả sử format VN: 1.250.000,50 -> 1250000.50
    clean_str = str(number).replace(".", "").replace(",", ".").strip()
    
    try:
        return float(clean_str)
    except ValueError:
        return 0.0
number = "2"
_parse_shopee_number(number)

def _parse_shopee_date(date):
    if not date:
       return date.today().strftime("%Y-%m-%d")
    parts = date.strip().split("/")
    if len(parts)==3:
        day, month, year = parts
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}" #zfill để luôn lắp đầy, ví dụ ngày = 1 thì thành 01
    else:
        return date
def import_from_csv(filepath, sku_id, sku_name, cogs):
    setup()
    import csv
    imported = 0
    skipped = 0
    
    try:
     with open("sample_shopee.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f) #giải mã file csv
        for row in reader: #đặt các giá trị vào file
           order_id = row.get("Mã đơn hàng", "").strip()
           revenue = row.get("Tổng số tiền người mua thanh toán", "0")
           platform_fee = row.get("Phí dịch vụ", "0")
           shipping_gap = row.get("Phí vận chuyển (Chênh lệch)", "0")
           order_date = row.get("Ngày đặt hàng", "")
           if order_date == False or revenue ==0:
              skipped +=1
           revenue = _parse_shopee_number(revenue)
           platform_fee = _parse_shopee_number(platform_fee)
           shipping_gap = _parse_shopee_number(shipping_gap)
           order_date = _parse_shopee_date(order_date)
           
           success = insert_order((
             order_id, sku_id, sku_name, "shopee",
             revenue, platform_fee, shipping_gap,
             cogs, order_date
           ))
           if success:
              imported +=1
           else:
              skipped+=1
     return (imported, skipped)
    except FileNotFoundError:
     print(f"  Không tìm thấy file: {filepath}")
     return (0, 0)
    except Exception as i:
        print(f"Lỗi ở {i}")
    


