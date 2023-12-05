#!/bin/bash

# 设置要执行的次数
number_of_runs=10

# 循环执行 redis-benchmark
for i in $(seq 1 $number_of_runs); do
    echo "Run $i" >>output.txt
    redis-benchmark -h 172.17.0.2 -p 6379 -t set,get -c 50 -n 10000 | grep "requests per second" >>output.txt
done
