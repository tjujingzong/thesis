#!/bin/bash

# 定义压力级别
cpu_levels=(20)
memory_levels=("1G" )
io_levels=(1 )

# 获取 Redis 容器的 PID
redis_pid=$(pidof redis-server)

# 实验结果保存目录
mkdir -p stress_test_results
result_file="stress_test_results/result_$(date +%Y%m%d%H%M%S).txt"

# 为当前用户配置无密码执行 perf stat 的权限
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat -p $redis_pid -o temp_result.txt sleep 30" | sudo tee /etc/sudoers.d/perf_stat_nopass


# 实验开始
echo "Starting stress tests..." | tee -a $result_file

for cpu in ${cpu_levels[@]}; do
    for mem in ${memory_levels[@]}; do
        for io in ${io_levels[@]}; do
            # 施加压力
            stress-ng --cpu $cpu --vm 1 --vm-bytes $mem --io $io --timeout 60s &

            # 等待一段时间以稳定压力
            sleep 10

            # 监控 Redis 性能
            echo "Monitoring under stress level: CPU=$cpu%, MEM=$mem, IO=$io" | tee -a $result_file
            sudo perf stat -p $redis_pid -o temp_result.txt sleep 30

            # 保存和输出结果
            echo "Results for CPU=$cpu%, MEM=$mem, IO=$io:" >> $result_file
            cat temp_result.txt >> $result_file
            echo "-------------------------------------------" >> $result_file

            # 清理
            pkill stress-ng
            sleep 10
        done
    done
done

# 实验结束
echo "Stress tests completed." | tee -a $result_file
