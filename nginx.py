import requests
import time

# Nginx服务器的URL
url = "http://localhost:8080"

# 存储每个请求的延时
delays = []

# 记录脚本开始运行的时间
start_time = time.time()

# 持续执行直到6秒结束
while time.time() - start_time < 6:
    # 记录请求开始的时间
    request_start = time.time()
    try:
        # 发送HTTP请求
        response = requests.get(url)
        # 计算这次请求的延时，并添加到列表中
        delay = time.time() - request_start
        delays.append(delay)
    except requests.exceptions.RequestException as e:
        # 如果请求失败，打印错误信息
        print(f"Request failed: {e}")

# 计算平均延时
average_delay = sum(delays) / len(delays) if delays else 0

print(average_delay * 1000)
