import csv


# 打开TXT文件并读取内容
with open('../results_redis/202312211754-redis_lan.txt', 'r') as txt_file:
    lines = txt_file.readlines()

# 创建CSV文件并写入数据
with open('../data_analyse/data_result/202312211754-redis_lan.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # 添加列名
    column_names = ['stress-vm', 'stress-cpu(%)', 'stress-io(%)', 'min-latency', 'max-latency', 'avg-latency', 'samples']
    csv_writer.writerow(column_names)

    # 将TXT数据转换成CSV格式并写入文件
    for line in lines:
        data = line.split()
        csv_writer.writerow(data)

print("文件已成功转换为CSV格式并添加列名。")
