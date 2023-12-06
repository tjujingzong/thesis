#!/bin/bash

# Define stress levels
# cpu_levels=(0 1 2 3)
# memory_levels=("1M" "512M" "1G" "1.5G" "2G" "2.5G" "3G" "3.5G")
# io_levels=(0 1 2 3 4 5)

# 初始化 memory_levels 数组
memory_levels=()

# 设置循环的起始值和上限（单位：MB）
start=1
limit=6145 # 6145

# 填充 memory_levels 数组
for ((mem = start; mem <= limit; mem += 256)); do
    memory_levels+=("${mem}M")
done

# Redis benchmark configuration
host="172.17.0.2"
port="6379"
benchmark_duration="20s"
monitor_duration="4" # 设置监控时长短于压力测试时长
benchmark_cmd="redis-benchmark -h $host -p $port -t get -c 50 -n 100000"

# Get the PID of the Redis container
redis_pid=$(pidof redis-server)

# Experiment result save directory
dir="results_redis"
mkdir -p $dir

# Current date and time for file naming
current_datetime=$(date +%Y%m%d%H%M)

# File paths
redis_cpi="$dir/redis_cpi_mem_$current_datetime.txt"
benchmark_result_file="$dir/redis_throughput_mem_$current_datetime.txt"
sys_result="$dir/redis_sys_mem_$current_datetime.txt"

# Configure sudoers for perf stat without a password
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass

# Starting experiments
echo "Starting stress tests..."

for mem in ${memory_levels[@]}; do
    # Apply stress in background
    stress-ng --vm 1 --vm-bytes $mem --timeout $benchmark_duration

    sleep 4
    # Start Redis benchmark in background and save its output
    start_time=$(date +%s) # 记录开始时间
    (
        for i in {1..3}; do
            $benchmark_cmd | grep "requests per second" >>$benchmark_result_file
        done
    ) &

    # Monitor Redis performance
    sudo perf stat -e cycles,instructions -x, -p $redis_pid -o temp1.txt sleep $monitor_duration &

    # Monitor system performance with perf
    sudo perf stat -d -x, -a -o temp2.txt sleep $monitor_duration

    # Cleanup
    wait
    end_time=$(date +%s)                # 记录结束时间
    duration=$((end_time - start_time)) # 计算持续时间
    echo "mem $mem $duration seconds" >>$benchmark_result_file
    pkill stress-ng
    pkill redis-benchmark
    cat temp1.txt >>$redis_cpi
    cat temp2.txt >>$sys_result
    sleep 1
done
echo "Stress tests completed."
# End of experiments
reset
