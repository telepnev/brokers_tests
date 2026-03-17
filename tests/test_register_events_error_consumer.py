import uuid

from kafka import KafkaProducer

from framework.internal.http.mail import MailApi


def test_register_events_error_consumer(mail: MailApi, kafka_producer: KafkaProducer) -> None:
    login = f"evgen_{uuid.uuid4().hex}"
    message = {
        "login": login,
        "email": f"{login}@bk.ru",
        "password": "1234567"
    }

    kafka_producer.send('register-events-errors', message)