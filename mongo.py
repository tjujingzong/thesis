from pymongo import MongoClient
import time

# MongoDB连接设置
host = "localhost"
port = 27017
dbname = "testdb"  # 测试数据库名
collection_name = "testcol"  # 测试集合名

# 连接到MongoDB
client = MongoClient(host, port)
db = client[dbname]
collection = db[collection_name]

# 确保集合里至少有一条数据
if collection.count_documents({}) == 0:
    collection.insert_one({"name": "test"})


# 测试延迟
def test_latency(duration=6):
    latencies = []
    end_time = start_time = time.time()
    while end_time - start_time < duration:
        query_start_time = time.time()
        collection.find_one()
        query_end_time = time.time()
        latency = (query_end_time - query_start_time) * 1000  # 毫秒
        latencies.append(latency)
        end_time = time.time()

    if latencies:  # 确保至少进行了一次查询
        avg_latency = sum(latencies) / len(latencies)
        print(f"{avg_latency:.6f}")
    else:
        print("No queries were performed.")


test_latency(6)
