#!/bin/bash

# Tomcat 服务器的 URL
URL="http://localhost:8080"

# 设置总运行时间限制（6秒）
TIME_LIMIT=7

# 初始化总延迟变量
total_delay=0
count=0

# 记录脚本开始时间
start_time=$(date +%s)

while :; do
    # 检查是否已超过时间限制
    current_time=$(date +%s)
    if ((current_time - start_time >= TIME_LIMIT)); then
        break
    fi

    # 发送请求并记录时间
    start=$(date +%s.%N)
    curl -o /dev/null -s $URL
    end=$(date +%s.%N)

    # 计算延迟
    delay=$(echo "$end - $start" | bc)
    total_delay=$(echo "$total_delay + $delay" | bc)

    # 计数请求次数
    count=$((count + 1))

    echo "Request $count: $delay seconds"
done

# 如果有请求被发送，计算平均延迟
if [ $count -gt 0 ]; then
    average_delay=$(echo "$total_delay / $count" | bc -l)
    echo "Average Delay: $average_delay seconds over $count requests"
else
    echo "No requests were made within the time limit."
fi
