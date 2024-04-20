import pandas as pd

# 读取CSV文件
df = pd.read_csv('data_result/00-all_data.csv')

# 删除cs (context switches/s)列
df = df.drop('cs (context switches/s)', axis=1)

# 列名映射字典
rename_dict = {
    'ipc': 'ipc',
    'context_switches(K/sec)': 'context_switches(K/s)',
    'cpu_migrations(/sec)': 'cpu_migrations(/s)',
    'page_faults(/sec)': 'page_faults(/s)',
    'branches(M/sec)': 'branches(M/s)',
    'branch_misses(%)': 'branch_misses(%)',
    'L1_dcache_loads(M/sec)': 'L1_dcache_loads(M/sec)',
    'L1_dcache_load_misses(%)': 'L1_dcache_load_misses(%)',
    'r (procs)': 'r_procs',
    'b (procs)': 'b_procs',
    'Swap (KB)': 'swap(KB)',
    'Free (KB)': 'free(KB)',
    'Buffers (KB)': 'buffers(KB)',
    'Cached (KB)': 'cached(KB)',
    'si (KB/s)': 'swap_in(KB/s)',
    'so (KB/s)': 'swap_out(KB/s)',
    'bi (blocks/s)': 'block_in(blocks/s)',
    'bo (blocks/s)': 'block_out(blocks/s)',
    'in (interrupts/s)': 'interrupts(/s)',
    'us (%)': 'user_time(%)',
    'sy (%)': 'system_time(%)',
    'id (%)': 'idle_time(%)',
    'wa (%)': 'iowait_time(%)',
    'st (%)': 'steal_time(%)'
}

# 使用字典重命名列
df.rename(columns=rename_dict, inplace=True)
df.drop('steal_time(%)', axis=1, inplace=True)
# 保存到新的CSV文件
df.to_csv('data_result/01-all_data.csv', index=False)
