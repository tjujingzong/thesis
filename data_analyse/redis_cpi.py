import re
import matplotlib.pyplot as plt


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_redis/redis_cpi_mem_202312062251.txt')
content = ''
for line in lines:
    content += line

pattern = r'(\d+\.\d+),insn per cycle'

cpi = re.findall(pattern, content)
print(cpi)


# 绘制图像
plt.plot(cpi)
plt.xlabel('memory stress(MB)')
# 横坐标从0开始 每次加256M

# 横坐标只在1024的倍数处显示
plt.xticks(range(0, len(cpi), 4), range(0, len(cpi) * 256, 1024))

plt.ylabel('insn per cycle')

# 保存图片
plt.savefig('../data_analyse/pic/redis_cpi_mem.png')
