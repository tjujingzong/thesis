# CPU 使用率
monitor_duration="4"
mpstat -P ALL 1 $monitor_duration >temp_cpu_usage.txt &

# 内存使用率
vmstat 1 $monitor_duration >temp_mem_usage.txt &

#  磁盘利用率
iostat 1 $monitor_duration >temp_disk_usage.txt &

# script -c "timeout 4 iftop -t" temp_iftop_output.txt
