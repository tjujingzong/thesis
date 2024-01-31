import csv

import re
import pandas as pd

# 打开TXT文件并读取内容
with open('../results_tomcat/202401252313-tomcat_lan.txt', 'r') as txt_file:
    lines = txt_file.readlines()

# 创建CSV文件并写入数据
with open('../data_analyse/data_result/202401252313-tomcat_lan.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # 添加列名
    column_names = ['stress-vm', 'stress-cpu(%)', 'stress-io(%)', 'avg-latency']
    csv_writer.writerow(column_names)

    # 将TXT数据转换成CSV格式并写入文件
    for line in lines:
        data = line.split()
        csv_writer.writerow(data)

print("文件已成功转换为CSV格式并添加列名。")


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_tomcat/202401252313-tomcat_sys.txt')
content = ''
for i in range(1, len(lines)):
    content += lines[i]

ipc_pattern = r'(\d+\.\d+),insn per cycle'
ipc = []
ipc = re.findall(ipc_pattern, content)
df = pd.DataFrame(ipc)
# 设置列名
df.columns = ['ipc']

context_switches_pattern = r'context-switches,.*?(\d+\.\d+),K/sec'
context_switches = []
context_switches = re.findall(context_switches_pattern, content)
df['context_switches(K/sec)'] = context_switches

cpu_migrations_pattern = r'cpu-migrations,.*?(\d+\.\d+),/sec'
cpu_migrations = []
cpu_migrations = re.findall(cpu_migrations_pattern, content)
df['cpu_migrations(/sec)'] = cpu_migrations

page_faults_pattern = r'page-faults,.*?(\d+\.\d+),K/sec|page-faults,.*?(\d+\.\d+),/sec'
page_faults = []
page_faults = re.findall(page_faults_pattern, content)
merged_page_faults = [float(pf[0]) * 1024 if pf[0] else float(pf[1]) for pf in page_faults]
df['page_faults(/sec)'] = merged_page_faults

branches_pattern = r'branches,.*?(\d+\.\d+),M/sec'
branches = []
branches = re.findall(branches_pattern, content)
df['branches(M/sec)'] = branches

branch_misses_pattern = r'branch-misses,.*?(\d+\.\d+),of all branches'
branch_misses = []
branch_misses = re.findall(branch_misses_pattern, content)
df['branch_misses(%)'] = branch_misses

#
L1_dcache_loads_pattern = r'L1-dcache-loads,.*?(\d+\.\d+),M/sec|L1-dcache-loads,.*?(\d+\.\d+),G/sec'
L1_dcache_loads = []
L1_dcache_loads = re.findall(L1_dcache_loads_pattern, content)
L1_dcache_loads = [float(ld[0]) if ld[0] else float(ld[1]) * 1024 for ld in L1_dcache_loads]
df['L1_dcache_loads(M/sec)'] = L1_dcache_loads

L1_dcache_load_misses_pattern = r'L1-dcache-load-misses,.*?(\d+\.\d+),of all L1-dcache accesses'
L1_dcache_load_misses = []
L1_dcache_load_misses = re.findall(L1_dcache_load_misses_pattern, content)
df['L1_dcache_load_misses(%)'] = L1_dcache_load_misses

# 保存cpi 为csv文件
df.to_csv("./data_result/202401252313-tomcat_sys.csv", index=False)

def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_tomcat/202401252313-tomcat_vmstate.txt')

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
with open('../data_analyse/data_result/202401252313-tomcat_vmstate.csv', 'w') as f:
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
df1 = pd.read_csv('../data_analyse/data_result/202401252313-tomcat_vmstate.csv', names=column_names_with_units)

# 保存
df1.to_csv('../data_analyse/data_result/202401252313-tomcat_vmstate.csv', index=False)

# 读取CSV文件
df1 = pd.read_csv('../data_analyse/data_result/202401252313-tomcat_lan.csv')
df2 = pd.read_csv('../data_analyse/data_result/202401252313-tomcat_sys.csv')
df3 = pd.read_csv('../data_analyse/data_result/202401252313-tomcat_vmstate.csv')

# df1仅保留avg-latency列
df1 = df1[['avg-latency']]
# 合并文件
combined_df = pd.concat([df2, df3, df1], axis=1)

# 将合并后的数据保存到新的CSV文件
combined_df.to_csv('../data_analyse/data_result/202401252313-tomcat-all_data.csv', index=False)
