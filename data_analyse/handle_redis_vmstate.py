import pandas as pd


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_redis/202312211754-redis_vmstate.txt')

content = ''
for i in range(1, len(lines)):
    if i % 8 != 0 and i % 8 != 1 and i % 8 != 2:
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
    if count == 5:
        # 计算平均值并格式化为逗号分隔的字符串
        avg_line = ','.join(f'{sum_val / count:.2f}' for sum_val in sums)
        averages.append(avg_line)

        # 重置总和和计数
        sums = None
        count = 0

# 将平均值写入文件
with open('../data_analyse/data_result/202312211406-redis_vmstate.csv', 'w') as f:
    f.write('\n'.join(averages))

# Assuming the csv file has data in the same order as the vmstat command output

# Adding units in parentheses
column_names_with_units = [
    'r (procs)', 'b (procs)', 'Swap (KB)', 'Free (KB)', 'Buffers (KB)', 'Cached (KB)',
    'si (KB/s)', 'so (KB/s)', 'bi (blocks/s)', 'bo (blocks/s)',
    'in (interrupts/s)', 'cs (context switches/s)',
    'us (%)', 'sy (%)', 'id (%)', 'wa (%)', 'st (%)'
]

# Reading the CSV file
df1 = pd.read_csv('../data_analyse/data_result/202312211406-redis_vmstate.csv', names=column_names_with_units)

# 保存
df1.to_csv('../data_analyse/data_result/202312211754-redis_vmstate.csv', index=False)
