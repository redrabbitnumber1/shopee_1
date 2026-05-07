import sqlite3
from set_up import (
    query_profit_by_channel,
    query_profit_by_sku,
    query_profit_by_month,
    query_total_summary,

)

db_name = "shopee_order.db"
def seperate_title(title):
    bar = "===" * 52
    print(bar + title + bar)

def show_summary():
 try:
  connect = None
  with sqlite3.connect(db_name) as connect:
    c = connect.cursor()

    row = query_total_summary() 
    tong_don, so_sku, so_channel, tong_dt, tong_profit = row[0]
    if tong_don == 0:
        print ("Không có dữ liệu")
        return False
    else:
        print("TỔNG QUAN")
        print(f"  Tổng đơn: {tong_don}")
        print(f"  Số SKU: {so_sku}")
        print(f"  Số channel: {so_channel}")
        print(f"  Tổng DT: {tong_dt:,.0f}đ")
        print(f"  Tổng profit: {tong_profit:,.0f}đ")
    if tong_profit <0:
        print("Đang lỗ")
    elif tong_profit >=0:
         if tong_dt == 0:
            margin = 0
         else:
            margin = (tong_profit/tong_dt * 100)
         print(f" Margin lợi nhuận{margin:.2f}%") #làm tròn đến chữ số thập phân thứ hai
    
 except Exception as e:
    print(f"Lỗi ở {e}")
 finally:
    connect.close()
    print("Ngắt kết nối thành công")

def show_by_channel():
   rows = query_profit_by_channel()
   if rows and rows[0][0] is not None:
      print("PROFIT THEO CHANNEL")
      print(" Channel | Đơn | Doanh thu | Profit | Margin")
      print("---")
      for row in rows:
       channel, don, dt, phi, von, profit, margin = row
       if float(profit) >= 0:
         icon = "✔️"
       else:
          icon = "X"
       print(f"{icon} {channel:<10} {don:>5} {dt:>14,.0f} {profit:>14,.0f} {margin:>6.1f}%")
         
   else: 
     print("Không có dữ liệu")


def show_by_sku():
   lo_list =[]
   loi_list =[]
   rows=query_profit_by_sku()
   if rows and rows[0][0] is not None:
      print("PROFIT THEO SKU")
      for row in rows:
       sku_id, name, don, profit, margin = row
       lo_list = [i for i in rows if float(profit) <0]
       loi_list =[i for i in rows if float(profit) >=0]
    
      print(f"SKU ĐANG LỖ {len(lo_list)}")
      for i in lo_list:
       sku_id, name, don, profit, margin = row
       print(f"✗ {sku_id} {name:<20} {don} đơn | Lỗ: {abs(profit):>10,.0f} đ ({margin}%)")
      
      print(f"SKU ĐANG LỜI {len(loi_list)}")
      for i in loi_list:
          sku_id, name, don, profit, margin = i
          print(f"   ✓ {sku_id} {name:<20} {don} đơn | Lời: {profit:>10,.0f} đ ({margin}%)")
      

   else: 
     print("Không có dữ liệu")


def show_by_month():
   rows = query_profit_by_month()
   with sqlite3.connect(db_name) as connect:
    c = connect.cursor()
    
    if rows and rows[0][0] is not None:
      print("PROFIT THEO THÁNG")
      max_profit = max(r[3] for r in rows) if rows else 1
      for thang, don, dt, profit in rows:
        # Normalize mỗi bar theo max_profit chung
        bar_len = int(profit / max_profit * 20)
        # 2024-01: 274000 / 274000 * 20 = 20  ← bar dài nhất
        # 2024-02: 139500 / 274000 * 20 = 10  ← bar ngắn hơn
        # 2024-03: 113000 / 274000 * 20 = 8   ← bar ngắn nhất
        
        bar = "█" * max(0, bar_len)
        print(f"  {thang}  {profit:>12,.0f}  {bar}")

    else: 
     print("Không có dữ liệu")

show_by_month()

   


    
    
    

    
