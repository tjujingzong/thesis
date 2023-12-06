host="172.17.0.2"
port="6379"
benchmark_cmd="redis-benchmark -h $host -p $port -t get -c 50 -n 100000"
start_time=$(date +%s) # 记录开始时间
(
    for i in {1..3}; do
        $benchmark_cmd | grep "requests per second" >>temp.txt
    done
) 
end_time=$(date +%s)                # 记录结束时间
duration=$((end_time - start_time)) # 计算持续时间
echo "Total duration: $duration seconds" >>temp.txt
