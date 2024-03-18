#!/bin/bash

memory_levels=()
for ((mem = 7168; mem >= 5632; mem -= 256)); do
    memory_levels+=("${mem}M")
done
# memory_levels+=("4k")
# cpu_levels=(100)
# io_levels=(100)
cpu_levels=(50 30 10 0)
io_levels=(30 20 10 1)

benchmark_duration="200"
monitor_duration="6" # 设置监控时长短于压力测试时长
dir="results_redis"
mkdir -p $dir
current_datetime=$(date +%Y%m%d%H%M)

# File paths
sys_result="$dir/$current_datetime-redis_sys.txt"
latency="$dir/$current_datetime-redis_lan.txt"
vmstate="$dir/$current_datetime-redis_vmstate.txt"

echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass
monitor_performance() {
    sleep 3
    docker exec -i "redis-server" timeout $monitor_duration redis-cli --latency >"redis_latency_results.txt" &
    local pid_redis=$!

    sudo perf stat -d -x, -a -o temp2.txt sleep $monitor_duration &
    local pid_perf=$!

    vmstat 1 $monitor_duration >temp_mem_usage.txt &
    local pid_vmstat=$!

    # 等待特定的后台进程
    wait $pid_redis
    wait $pid_perf
    wait $pid_vmstat

    # Cleanup
    echo "end monitor"
    pkill stress-ng
    cat temp2.txt >>$sys_result
    cat "redis_latency_results.txt" >>$latency
    cat temp_mem_usage.txt >>$vmstate
    sleep 1
}

# Starting experiments
echo "Starting stress tests..."

for io in ${io_levels[@]}; do
    for cpu in ${cpu_levels[@]}; do
        for mem in ${memory_levels[@]}; do
            # Apply stress in background
            printf "$mem $cpu $io " >>$latency
            sleep 2
            stress-ng --cpu 4 --cpu-load $cpu --vm 2 --vm-bytes $mem --iomix 2 --iomix-bytes $io% --timeout $benchmark_duration &
            monitor_performance &
            wait
        done
    done
done

echo "Stress tests completed."
# End of experiments
reset
