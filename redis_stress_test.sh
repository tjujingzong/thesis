#!/bin/bash

# Define stress levels
# cpu_levels=(0 1 2 3)
# memory_levels=("1M" "512M" "1G" "1.5G" "2G" "2.5G" "3G" "3.5G")
# io_levels=(0 1 2 3 4 5)

# cpu_levels=(0)
# io_levels=(0)
memory_levels=("1M")

# Redis benchmark configuration
redis_host="172.17.0.2"
redis_port="6379"
benchmark_duration="20s"
benchmark_cmd=" redis-benchmark -h $redis_host -p $redis_port -t get -c 100 -n 100000"

# Get the PID of the Redis container
redis_pid=$(pidof redis-server)

# Experiment result save directory
mkdir -p stress_test_results
redis_cpi="stress_test_results/redis_cpi_$(date +%Y%m%d%H%M).txt"
benchmark_result_file="stress_test_results/redis_benchmark_result_$(date +%Y%m%d%H%M).txt"
sys_result="stress_test_results/redis_sys_$(date +%Y%m%d%H%M).txt"

# Configure sudoers for perf stat without a password
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass

# Starting experiments
echo "Starting stress tests..."

for mem in ${memory_levels[@]}; do

    # Apply stress
    stress-ng --vm 1 --vm-bytes $mem --timeout $benchmark_duration
    # Wait for the stress and benchmark to stabilize
    sleep 3
    # Start Redis benchmark in background and save its output
    $benchmark_cmd | grep "requests per second">$benchmark_result_file

    # Monitor Redis performance
    sudo perf stat -e cycles,instructions -x, -p $redis_pid -o $redis_cpi sleep 3

    # Monitor system performance with perf
    sudo perf stat -d -x, -a -o $sys_result sleep 3

    # Cleanup
    pkill stress-ng
    pkill redis-benchmark
    sleep 3
done

# End of experiments
echo "Stress tests completed."
