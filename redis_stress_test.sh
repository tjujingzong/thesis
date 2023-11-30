#!/bin/bash

# Define stress levels
cpu_levels=(0)
memory_levels=("1M")
io_levels=(0)

# Redis benchmark configuration
redis_host="172.17.0.2"
redis_port="6379"
benchmark_duration="20s"
benchmark_cmd=" redis-benchmark -h $redis_host -p $redis_port -t set,get -c 50 -n 100000 -r 10000 -l"

# Get the PID of the Redis container
redis_pid=$(pidof redis-server)

# Experiment result save directory
mkdir -p stress_test_results
result_file="stress_test_results/redis_result_$(date +%Y%m%d%H%M).txt"
benchmark_result_file="stress_test_results/redis_benchmark_result_$(date +%Y%m%d%H%M).txt"

# Configure sudoers for perf stat without a password
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/perf stat" | sudo tee /etc/sudoers.d/perf_stat_nopass

# Starting experiments
echo "Starting stress tests..."

for cpu in ${cpu_levels[@]}; do
    for mem in ${memory_levels[@]}; do
        for io in ${io_levels[@]}; do
            # Apply stress
            stress-ng --cpu $cpu --vm 1 --vm-bytes $mem --io $io --timeout $benchmark_duration &

            # Start Redis benchmark in background and save its output
            $benchmark_cmd >$benchmark_result_file &

            # Wait for the stress and benchmark to stabilize
            sleep 3

            # Monitor Redis performance
            echo "CPU=$cpu, MEM=$mem, IO=$io, BENCHMARK=running" | tee -a $result_file
            sudo perf stat -e cycles,instructions -x, -p $redis_pid -o temp_result.txt sleep $benchmark_duration

            # Monitor system performance with perf
            sudo perf stat -d -x, -a -o system_performance.txt sleep $benchmark_duration

            # Save and output results
            cat temp_result.txt >>$result_file
            cat system_performance.txt >>$result_file
            cat $benchmark_result_file | tail -n 3 >>$result_file
            echo "-------------------------------------------" >>$result_file

            # Cleanup
            pkill stress-ng
            pkill redis-benchmark
            sleep 3
        done
    done
done

# End of experiments
echo "Stress tests completed."
