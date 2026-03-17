import json
import uuid

from kafka import KafkaConsumer, KafkaProducer


def extract_items(data):
    """Разворачивает любые вложенные списки"""
    if isinstance(data, dict):
        return [data]

    if isinstance(data, list):
        result = []
        for item in data:
            result.extend(extract_items(item))
        return result

    return []


def test_success_registration_with_kafka_producer_consumer(kafka_producer: KafkaProducer):
    login = f"evgen_{uuid.uuid4().hex}"

    kafka_producer.send("register-events", {
        "login": login,
        "email": f"{login}@bk.ru",
        "password": "1234567"
    })

    consumer = KafkaConsumer(
        "register-events",
        bootstrap_servers=["185.185.143.231:9092"],
        auto_offset_reset="latest",
        # auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    found = False

    for msg in consumer:
        items = extract_items(msg.value)

        for item in items:
            if item.get("login") == login:
                found = True
                print(item.get("login"))
                break

        if found:
            break

    assert found, "User not found in Kafka"

    consumer.close()
