import mysql.connector
import time

# MySQL连接设置
host = "localhost"
port = 3306
user = "root"  # 你的MySQL用户名
password = "123456"  # 你的MySQL密码
database = "testdb"  # 测试数据库名
table_name = "testtable"  # 测试表名

# 连接到MySQL
cnx = mysql.connector.connect(
    user=user, password=password, host=host, database=database, port=port
)

cursor = cnx.cursor()

# 确保表中至少有一条数据
cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
row_count = cursor.fetchone()[0]
# print(row_count)
if row_count == 0:
    cursor.execute(f"INSERT INTO {table_name} (name) VALUES ('test')")
    cnx.commit()


# 测试延迟
def test_latency(duration=6):
    latencies = []
    end_time = start_time = time.time()
    while end_time - start_time < duration:
        query_start_time = time.time()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        result = cursor.fetchall()
        query_end_time = time.time()
        latency = (query_end_time - query_start_time) * 1000  # 毫秒
        latencies.append(latency)
        end_time = time.time()

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        print(f"{avg_latency:.6f}")
    else:
        print("No queries were performed.")


test_latency(6)

# 关闭连接
cursor.close()
cnx.close()
