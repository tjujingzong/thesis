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

    #Tomcat 服务器的 URL
    URL="http://localhost:8080"

    # 设置总运行时间限制（6秒）
    TIME_LIMIT=$monitor_duration

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
    done
    average_delay=$(echo "$total_delay / $count*1000" | bc -l)
    echo "$average_delay" >"tomcat_response_time.txt"
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
