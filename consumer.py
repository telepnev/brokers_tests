import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "register-events",
    bootstrap_servers=["185.185.143.231:9092"],
    auto_offset_reset="earliest",                   # самые ранние сообщения
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

for message in consumer:
    print(message.value['login'])
