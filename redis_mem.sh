#!/bin/bash

memory_levels=("4K")
for ((mem = 256; mem <= 7680; mem += 512)); do
    memory_levels+=("${mem}M")
done

cpu_levels=(0 1 2 3 4)
io_levels=(0 1 2 3 4)

benchmark_duration="15"
monitor_duration="6" # 设置监控时长短于压力测试时长
dir="results_redis"
mkdir -p $dir
current_datetime=$(date +%Y%m%d%H%M)

# File paths
sys_result="$dir/redis_sys_$current_datetime.txt"
latency="$dir/redis_lan_$current_datetime.txt"
vmstate="$dir/redis_vmstate_$current_datetime.txt"

echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass
monitor_performance() {
    sleep 6
    (
        echo "start monitoring......"
        docker exec -i "redis-server" timeout $monitor_duration redis-cli --latency >"redis_latency_results.txt"
    ) &

    sudo perf stat -d -x, -a -o temp2.txt sleep $monitor_duration &
    vmstat 1 $monitor_duration >temp_mem_usage.txt &

    # Cleanup
    wait
    pkill stress-ng
    cat temp2.txt >>$sys_result
    cat "redis_latency_results.txt" >>$latency
    cat temp_mem_usage.txt >>$vmstate
    sleep 2
}

# Starting experiments
echo "Starting stress tests..."

for io in ${io_levels[@]}; do
    for cpu in ${cpu_levels[@]}; do
        for mem in ${memory_levels[@]}; do
            # Apply stress in background
            stress-ng --cpu $cpu --vm 2 --vm-bytes $mem --io $io --timeout $benchmark_duration &
            monitor_performance
        done
    done
done

echo "Stress tests completed."
# End of experiments
reset
