def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../data_analyse/data_result/redis_vmstate.txt')

content = ''
for i in range(1, len(lines)):
    if i % 8 != 0 and i % 8 != 1:
        content += lines[i]

print(content)
# 将数据按行分割
lines = content.strip().split('\n')

# 初始化用于累计和计数的变量
sums = None
count = 0
averages = []

# 遍历每行
for line in lines:
    # 将行分割成数字
    numbers = list(map(int, line.split()))

    # 如果是第一行，初始化总和列表
    if sums is None:
        sums = [0] * len(numbers)

    # 累加当前行的值
    sums = [sum_val + num for sum_val, num in zip(sums, numbers)]
    count += 1

    # 每6行计算一次平均值
    if count == 6:
        # 计算平均值并格式化为逗号分隔的字符串
        avg_line = ','.join(f'{sum_val / count:.2f}' for sum_val in sums)
        averages.append(avg_line)

        # 重置总和和计数
        sums = None
        count = 0

# 将平均值写入文件
with open('../data_analyse/data_result/redis_vmstate.csv', 'w') as f:
    f.write('\n'.join(averages))
