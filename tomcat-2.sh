#!/bin/bash

# 定义测试参数
memory_levels=()

for ((mem = 7168; mem > 0; mem -= 256)); do
    memory_levels+=("${mem}M")
done
cpu_levels=(50 30 10 0)
io_levels=(30 20 10 1)

memory_levels+=("4k")
# cpu_levels=(100)
# io_levels=(100)
benchmark_duration="200"
monitor_duration="6" # 监控时长短于压力测试时长
dir="results_tomcat"
mkdir -p $dir
current_datetime=$(date +%Y%m%d%H%M)

# 文件路径
sys_result="$dir/$current_datetime-tomcat_sys.txt"
latency="$dir/$current_datetime-tomcat_lan.txt"
vmstate="$dir/$current_datetime-tomcat_vmstate.txt"

# 准备性能监控
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass

monitor_performance() {
    sleep 3
    /bin/python3 tomcat.py >"tomcat_latency_results.txt" &
    local pid_tomcat=$!

    sudo perf stat -d -x, -a -o temp2.txt sleep $monitor_duration &
    local pid_perf=$!

    vmstat 1 $monitor_duration >temp_mem_usage.txt &
    local pid_vmstat=$!

    wait $pid_tomcat
    wait $pid_perf
    wait $pid_vmstat

    # 清理与结果汇总
    echo "end monitor"
    pkill stress-ng
    cat temp2.txt >>$sys_result
    cat "tomcat_latency_results.txt" >>$latency
    cat temp_mem_usage.txt >>$vmstate
    sleep 1
}

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
