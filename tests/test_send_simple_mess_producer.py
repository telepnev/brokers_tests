import json
import time
import uuid

from kafka import KafkaProducer
from framework.internal.http.mail import MailApi


def test_success_registration_with_kafka_producer(mail: MailApi, kafka_producer: KafkaProducer) -> None:
    login = f"evgen_{uuid.uuid4().hex}"
    message = {
        "login": login,
        "email": f"{login}@bk.ru",
        "password": "1234567"
    }

    kafka_producer.send('register-events', message)

    for _ in range(5):
        response = mail.find_message(query=login)
        if response.json()["total"] > 0:
            break
        time.sleep(1)
    else:
        raise AssertionError("Mail not found")
