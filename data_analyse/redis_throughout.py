# 读取results_redis/redis_throughput_mem_202312062251.txt
import re
import matplotlib.pyplot as plt


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_redis/redis_throughput_mem_202312062251.txt')
content = ''
for line in lines:
    content += line

pattern = r'\b\d+\.\d+\b'

result = re.findall(pattern, content)
print(result)

avg_throughout = []
for i in range(len(result)):
    # 每三个一组计算均值
    if i % 3 == 0:
        avg = (float(result[i]) + float(result[i + 1]) + float(result[i + 2])) / 3
        avg_throughout.append(avg)

print(avg_throughout)

# 绘制图像
plt.plot(avg_throughout)
plt.xlabel('memory stress(MB)')
# 横坐标从0开始 每次加256M

# 横坐标只在1024的倍数处显示
plt.xticks(range(0, len(avg_throughout), 4), range(0, len(avg_throughout) * 256, 1024))

plt.ylabel('throughout(req/s)')

# 保存图片
plt.savefig('../data_analyse/pic/redis_throughput_mem.png')
