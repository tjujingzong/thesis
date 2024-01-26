#!/bin/bash

memory_levels=("4K")
for ((mem = 7168; mem > 0; mem -= 256)); do
    memory_levels+=("${mem}M")
done

# cpu_levels=(0)
# io_levels=(1)
cpu_levels=(50 30 10 0)
io_levels=(30 20 10 1)

benchmark_duration="200"
monitor_duration="6" # 设置监控时长短于压力测试时长
dir="results_tomcat"
mkdir -p $dir
current_datetime=$(date +%Y%m%d%H%M)

sys_result="$dir/$current_datetime-tomcat_sys.txt"
latency="$dir/$current_datetime-tomcat_lan.txt"
vmstate="$dir/$current_datetime-tomcat_vmstate.txt"

echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass
calculate_average_latency() {
    total_latency=0

    # 对于每一秒，执行一次 curl 请求并累加响应时间
    for i in $(seq 1 $monitor_duration); do
        latency=$(curl -o /dev/null -s -w "%{time_total}" http://localhost:8080/your_tomcat_endpoint)
        total_latency=$(echo "$total_latency + $latency" | bc)
        sleep 1
    done

    # 计算平均延迟
    avg_latency=$(echo "scale=5; $total_latency / $monitor_duration" | bc)
    echo "$avg_latency" >"tomcat_response_time.txt"
}
monitor_performance() {
    sleep 3
    # 替换为监控 Tomcat 性能的命令
    calculate_average_latency &
    local pid_tomcat=$!

    sudo perf stat -d -x, -a -o temp2.txt sleep $monitor_duration &
    local pid_perf=$!

    vmstat 1 $monitor_duration >temp_mem_usage.txt &
    local pid_vmstat=$!

    # 等待特定的后台进程
    wait $pid_tomcat
    wait $pid_perf
    wait $pid_vmstat

    # Cleanup
    echo "end monitor"
    pkill stress-ng
    cat temp2.txt >>$sys_result
    cat "tomcat_response_time.txt" >>$latency
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
