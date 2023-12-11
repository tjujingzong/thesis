# CPU 使用率
monitor_duration="4"
# mpstat -P ALL 1 $monitor_duration >temp_cpu_usage.txt &

# # # 内存使用率
# # vmstat 1 $monitor_duration >temp_mem_usage.txt &

# #  磁盘利用率
# iostat 1 $monitor_duration >temp_disk_usage.txt &

vmstat 1 $monitor_duration > temp_mem_usage.txt &
stress-ng --cpu 1 --timeout $monitor_duration


# script -c "timeout 4 iftop -t" temp_iftop_output.txt

#!/bin/bash

# # 设置 Docker 容器名称
# CONTAINER_NAME="redis-server"

# # 设置延迟监控时间（秒）
# MONITOR_DURATION=3

# # 设置结果输出文件
# OUTPUT_FILE="redis_latency_results.txt"

# echo "开始监控 Redis 延迟，持续时间：$MONITOR_DURATION 秒"
# echo "监控结果将被保存到 $OUTPUT_FILE"

# # 使用 docker exec 在容器内运行 redis-cli --latency
# # 使用 timeout 命令来限制执行时间
# # 将输出重定向到宿主机的文件
# docker exec -i $CONTAINER_NAME timeout $MONITOR_DURATION redis-cli --latency latest >> 1.txt

# echo "延迟监控完成，结果已保存到 $OUTPUT_FILE"
