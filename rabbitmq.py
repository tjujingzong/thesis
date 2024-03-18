import pika
import time

# RabbitMQ连接参数
parameters = pika.ConnectionParameters(
    "localhost", 5672, "/", pika.PlainCredentials("guest", "guest")
)

# 建立连接
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明队列
queue_name = "test_queue"
channel.queue_declare(queue=queue_name)


# 发送消息，并在6秒内循环运行，最后计算平均延时
def publish_message_with_timeout(timeout=6):
    start_time = time.time()
    delays = []

    while time.time() - start_time < timeout:
        message_start_time = time.time()
        message = f"Message at {message_start_time}"
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        message_end_time = time.time()
        delays.append(message_end_time - message_start_time)

    # 如果有延时记录，则计算平均延时；否则，返回0
    return sum(delays) / len(delays) if delays else 0


# 测试发送消息并记录平均延时
average_delay = publish_message_with_timeout()
print(f"{average_delay*1000:.6f}")


# 接收消息的部分保持不变
def callback(ch, method, properties, body):
    print(f"Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
