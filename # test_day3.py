# test_day3.py
import sys
sys.stdout.reconfigure(encoding='utf-8')
from set_up import table_shopee_profit, insert_order,connecting

print("=== TEST NGÀY 3 ===\n")

# Setup database
table_shopee_profit()

# Test data — 5 orders khác nhau
test_orders = [
    ("ORD001", "SKU_A", "Áo thun", "shopee", 250000, 25000, 8000, 150000, "2024-01-15"),
    ("ORD002", "SKU_A", "Áo thun", "tiktok", 310000, 18600, 5000, 150000, "2024-01-15"),
    ("ORD003", "SKU_B", "Quần", "shopee", 180000, 18000, 9000, 120000, "2024-01-16"),
    ("ORD004", "SKU_B", "Quần", "lazada", 95000, 21450, 7000, 120000, "2024-01-16"),
    ("ORD005", "SKU_A", "Áo thun", "shopee", 250000, 25000, 8000, 150000, "2024-01-17"),
]
# Test 1: Insert 5 orders
print("Test 1: Insert 5 orders")
for order in test_orders:
    success = insert_order(order)
    status = "Correct" if success else "Not Correct"
    print(f"  {status} Insert {order[0]}")
# Test 2: Verify SELECT lại được dữ liệu
print("\nTest 2: SELECT lại 5 orders từ database")
conn = connecting()
cursor = conn.cursor()
cursor.execute("SELECT order_id, sku_id, channel, revenue FROM ordering")
rows = cursor.fetchall()
print(f"Total orders: {len(rows)}")
for row in rows:
    print(f"  {row}")
# Expected output:
# Total orders: 5
# ('ORD001', 'SKU_A', 'shopee', 250000.0)
# ('ORD002', 'SKU_A', 'tiktok', 310000.0)
# ...

conn.close()

# Test 3: Insert duplicate — phải fail
print("\nTest 3: Insert duplicate order_id (phải fail)")
duplicate = insert_order(("ORD001", "SKU_X", "Product X", "shopee",
                         100000, 10000, 5000, 50000, "2024-01-18"))
if not duplicate:
    print("  ✓ Duplicate order_id reject (return False)")
else:
    print("  ✗ ERROR: Duplicate không được reject!")

# Test 4: Count orders in database
print("\nTest 4: Đếm tổng orders")
conn = connecting()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM ordering")
count = cursor.fetchone()[0]
print(f"  Total: {count} orders (expected: 5)")
conn.close() 
print("\n✓ Tất cả test xong!")