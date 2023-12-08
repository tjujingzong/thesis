import re
import matplotlib.pyplot as plt


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_redis/redis_cpi_mem_202312072211.txt')
content = ''
pattern = r'(\d+\.\d+),insn per cycle'
cpi = []
for i in range(1, len(lines)):
    if i % 4 == 3:
        print(lines[i])
        # 如果line[i]中有符合pattern的 则加入cpi
        result = re.findall(pattern, lines[i])
        if result:
            cpi.append(float(result[0]))
        else:
            cpi.append(0)

print(len(cpi))

import pandas as pd

df = pd.DataFrame(cpi)
# 保存cpi 为csv文件
df.to_csv("./data_result/redis_cpi_mem.csv", index=False, header=False)


# 绘制散点图 值为0的不显示
# 创建一个索引数组，只包含非0值的索引
non_zero_indices = [i for i, x in enumerate(cpi) if x != 0]

# 使用这些索引来获取非0的cpi值和相应的横坐标
non_zero_cpi = [cpi[i] for i in non_zero_indices]
x_values = [i * 256 for i in non_zero_indices]  # 假设每个索引代表256MB

plt.scatter(x_values, non_zero_cpi, s=10, marker='o')

plt.xlabel('memory stress(MB)')
# 横坐标从0开始 每次加256M

# 横坐标只在1024的倍数处显示
plt.xticks(range(0, max(x_values) + 1, 1024), range(0, max(x_values) + 1, 1024))

plt.ylabel('insn per cycle')

# 保存图片
plt.savefig('../data_analyse/pic/redis_cpi_mem.png')
