import re
import pandas as pd


def read_file(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    return lines


lines = read_file('../results_redis/202312211754-redis_sys.txt')
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
df.to_csv("./data_result/202312211754-redis_sys.csv", index=False)
