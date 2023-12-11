# 基于机器学习的应用性能预测方法及实现
### 简介
本设计致力于分析不同类型应用在不同系统压力数据时性能指标的变化，收集系统压力数据与应用性能指标数据，通过收集和整理应用系统基础数据，利用机器学习模型来构建不同类型应用的性能预测模型，并对模型进行训练和验证，进而达到使用预测模型建立虚拟的应用性能模型，为大规模集群仿真调度提供依据。


### 常用命令
free -g -h

df -h

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-server

docker exec -it "redis-server" timeout 10 redis-cli --latency

redis-benchmark -h 172.17.0.2 -p 6379 -t get -c 50 -n 100000

redis-benchmark -h 172.17.0.2 -p 6379 -t set,get -c 50 -n 10000 -l| grep "requests per second" > output.txt


stress-ng --cpu $cpu --vm 1 --vm-bytes $mem --io $io --timeout $benchmark_duration


    # Start Redis benchmark in background and save its output
    (
        echo "start monitoring......"
        # for i in {1..3}; do
        #     $benchmark_cmd | grep "requests per second" >>$benchmark_result_file
        # done
        docker exec -i "redis-server" timeout $monitor_duration redis-cli --latency >"redis_latency_results.txt"
    ) &

    # Monitor Redis performance
    # sudo perf stat -e cycles,instructions -x, -p $redis_pid -o temp1.txt sleep $monitor_duration &


### 备注
如果在 redis-benchmark 命令中省略了 -t 选项，redis-benchmark 将会运行所有默认的基准测试，而不是仅限于特定的操作（如 SET 或 GET）。这意味着它将对 Redis 支持的各种操作进行性能测试，包括但不限于 SET, GET, INCR, LPUSH, LPOP, SADD, SPOP, LPUSH (后接 LRANGE), 和 MSET（根据 Redis 版本，可能还包括其他操作）。

性能问题：当虚拟机配置的内存超过宿主机的物理内存时，多出来的部分将使用交换空间（swap space），即硬盘空间作为虚拟内存。硬盘的读写速度远低于物理内存，因此这会严重影响虚拟机的性能。

& 表示后台运行

如果在使用 redis-benchmark 时不指定 -d 选项，默认的数据大小是 3 字节。这意味着每次 SET 操作存储的数据将默认为 3 字节大小。这个默认值很小，主要是为了快速测试 Redis 的响应时间和吞吐量，而不是为了压力测试或评估内存使用。

因此，如果你想测试 Redis 在处理更大数据量时的性能，建议使用 -d 选项来指定一个较大的数据大小。例如，使用 -d 1000 来测试每个键存储 1KB 数据的场景。这样的测试更能反映 Redis 在实际应用中的表现，特别是对于内存使用和处理大数据负载的能力。

您提供的是 vmstat 命令的输出格式，这是一种在许多 Unix/Linux 系统上用于监控虚拟内存、进程、CPU活动等的工具。下面是对输出中各个指标的解释：

procs (进程):

r: 运行队列中的进程数，即正在运行或等待CPU的进程数量。
b: 等待IO的进程数，即被阻塞的进程数量。
memory (内存):

交换 (swpd): 使用的虚拟内存量。
空闲 (free): 可用内存量。
缓冲 (buff): 作为缓冲区的内存量。
缓存 (cache): 作为缓存的内存量。
swap (交换区):

si: 从交换区到内存的交换速率（每秒读取的数量）。
so: 从内存到交换区的交换速率（每秒写入的数量）。
io (输入/输出):

bi: 块设备每秒接收的块数（块读取）。
bo: 块设备每秒发送的块数（块写入）。
system (系统):

in: 每秒的中断数，包括时钟中断。
cs: 每秒的上下文切换数。
cpu (处理器):

us: 用户时间百分比，用户进程执行时间占CPU总时间的比例。
sy: 系统时间百分比，内核进程执行时间占CPU总时间的比例。
id: 空闲时间百分比，无任务执行时CPU的空闲时间比例。
wa: 等待IO时间百分比，CPU等待IO完成的时间比例。
st: 被偷取的时间百分比（通常在虚拟环境中），其他虚拟机占用的CPU时间比例。

您提供的是 mpstat 命令的输出结果，这是一个在多核处理器系统中监控各个 CPU 性能的工具。输出结果展示了 CPU 的使用情况，包括各种类型的时间消耗。下面是输出结果中各项指标的含义：

平均时间: 这是一个时间标签，表示这些数据是在某个时间间隔内的平均值。

CPU:

all: 所有CPU的平均数据。
0, 1, 2, ...: 单个CPU的数据，数字代表具体的CPU编号。
%usr: 用户空间占用的CPU时间百分比。这是执行用户进程的时间比例（不包括低优先级进程）。

%nice: 用户空间内低优先级进程（nice进程）占用的CPU时间百分比。

%sys: 内核空间占用的CPU时间百分比。这是执行内核进程和中断的时间比例。

%iowait: IO等待时间占用的CPU时间百分比。这是CPU等待磁盘IO完成而未执行其他任务的时间比例。

%irq: 硬中断占用的CPU时间百分比。

%soft: 软中断占用的CPU时间百分比。

%steal: 虚拟环境中，虚拟CPU等待实际CPU资源的时间百分比（在云环境中比较常见）。

%guest: 运行虚拟处理器时占用的CPU时间百分比。

%gnice: 运行低优先级的虚拟处理器时占用的CPU时间百分比。

%idle: CPU空闲时间的百分比。这是CPU未被任何进程使用的时间比例。


您提到的 iostate 命令，我假设您指的是 iostat 命令，这是一个用于监控系统输入/输出设备和 CPU 使用情况的工具。让我们分析一下您提供的输出结果：

avg-cpu: 这一部分显示了CPU的平均使用情况。

%user: CPU处理用户级进程的时间百分比（不包括 nice 进程）。
%nice: CPU处理优先级较低的用户级进程的时间百分比。
%system: CPU处理系统级（内核）进程的时间百分比。
%iowait: CPU等待输入/输出完成时间的百分比。
%steal: 在虚拟化环境中，其他操作系统占用的CPU时间百分比。
%idle: CPU空闲时间的百分比。
在您的示例中，大部分时间CPU都处于空闲状态（95.13%），用户空间和系统空间的使用相对较低。

Device: 这部分显示了每个物理或虚拟设备的I/O统计数据。

tps (Transactions Per Second): 每秒I/O事务数。事务通常是指读取或写入操作。
kB_read/s: 每秒从设备读取的数据量（千字节/秒）。
kB_wrtn/s: 每秒写入设备的数据量（千字节/秒）。
kB_dscd/s: 每秒丢弃的数据量（千字节/秒）。
kB_read: 总共从设备读取的数据量（千字节）。
kB_wrtn: 总共写入设备的数据量（千字节）。
kB_dscd: 总共丢弃的数据量（千字节）。
在您的输出中，具体的设备I/O统计数据没有被提供。这些统计数据对于理解特定设备的负载和性能非常有用，尤其是在诊断磁盘I/O瓶颈或系统性能问题时。

总的来说，iostat 提供了有关CPU使用和I/O性能的关键信息，这对于系统管理员和性能分析人员来说非常宝贵。通过这些数据，可以识别出系统中可能存在的性能瓶颈和资源使用不平衡的问题。