# 基于机器学习的应用性能预测方法及实现
### 简介
本设计致力于分析不同类型应用在不同系统压力数据时性能指标的变化，收集系统压力数据与应用性能指标数据，通过收集和整理应用系统基础数据，利用机器学习模型来构建不同类型应用的性能预测模型，并对模型进行训练和验证，进而达到使用预测模型建立虚拟的应用性能模型，为大规模集群仿真调度提供依据。


### 常用命令
free -g -h

df -h

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-server


redis-benchmark -h 172.17.0.2 -p 6379 -t get -c 50 -n 100000

redis-benchmark -h 172.17.0.2 -p 6379 -t set,get -c 50 -n 10000 -l| grep "requests per second" > output.txt


stress-ng --cpu $cpu --vm 1 --vm-bytes $mem --io $io --timeout $benchmark_duration

### 备注
如果在 redis-benchmark 命令中省略了 -t 选项，redis-benchmark 将会运行所有默认的基准测试，而不是仅限于特定的操作（如 SET 或 GET）。这意味着它将对 Redis 支持的各种操作进行性能测试，包括但不限于 SET, GET, INCR, LPUSH, LPOP, SADD, SPOP, LPUSH (后接 LRANGE), 和 MSET（根据 Redis 版本，可能还包括其他操作）。

性能问题：当虚拟机配置的内存超过宿主机的物理内存时，多出来的部分将使用交换空间（swap space），即硬盘空间作为虚拟内存。硬盘的读写速度远低于物理内存，因此这会严重影响虚拟机的性能。

& 表示后台运行

如果在使用 redis-benchmark 时不指定 -d 选项，默认的数据大小是 3 字节。这意味着每次 SET 操作存储的数据将默认为 3 字节大小。这个默认值很小，主要是为了快速测试 Redis 的响应时间和吞吐量，而不是为了压力测试或评估内存使用。

因此，如果你想测试 Redis 在处理更大数据量时的性能，建议使用 -d 选项来指定一个较大的数据大小。例如，使用 -d 1000 来测试每个键存储 1KB 数据的场景。这样的测试更能反映 Redis 在实际应用中的表现，特别是对于内存使用和处理大数据负载的能力。