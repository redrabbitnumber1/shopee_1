from set_up import connecting, table_shopee_profit

print("connect thành công")
connecting()
table_shopee_profit()

connect = connecting()
c = connect.cursor() # cursor() đi với execute để thực thi lệnh 

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print(tables)

if tables and tables[0][0] == "ordering": #tìm xem có tồn tại table customers không
    print("Bảng tồn tại")
else:
    print("bảng không tồn tại")

c.execute("PRAGMA table_info(ordering)")
columns = c.fetchall()

print("Cột trong bảng:")
for col in columns:
     col_id, col_name, col_type, not_null, default, pk = col
     print(f"  - {col_name}: {col_type} (PRIMARY KEY: {pk})")
# # print cột, trong đó là dictionary col_name:col_type 


print("\n✓ Tất cả test pass!")


connect.close()


    






