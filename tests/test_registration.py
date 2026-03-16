import json
import time
import uuid

from kafka import KafkaProducer
from framework.internal.http.account import AccountApi
from framework.internal.http.mail import MailApi

"""
Пример опрос состояния
"""


def test_failed_registration(account: AccountApi, mail: MailApi) -> None:
    expected_mail = "evgen_123@bk.ru"
    account.register_user(
        login="string",
        email=expected_mail,
        password="string"
    )

    for _ in range(5):
        response = mail.find_message(query=expected_mail)
        if response.json()["total"] > 0:
            raise AssertionError("Mail not found")
        time.sleep(1)


def test_success_registration(account: AccountApi, mail: MailApi) -> None:
    login = f"evgen_{uuid.uuid4().hex}"

    account.register_user(
        login=login,
        email=f"{login}@bk.ru",
        password="1234567"
    )

    for _ in range(5):
        response = mail.find_message(query=login)
        if response.json()["total"] > 0:
            break
        time.sleep(1)
    else:
        raise AssertionError("Mail not found")


def test_success_registration_with_kafka_producer(mail: MailApi):
    login = f"evgen_{uuid.uuid4().hex}"
    message = {
        "login": login,
        "email": f"{login}@bk.ru",
        "password": "1234567"
    }

    producer = KafkaProducer(
        bootstrap_servers=["185.185.143.231:9092"],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks="all",                         # сколько брокеров должны подтвердить запись ("all" - самое безопасное, сообщение точно записано == Но медленнее)
        retries=5,                          # попробует повторить 5 раз.
        retry_backoff_ms=5000,              # Пауза между retries. Producer будет ждать 5 секунд перед повтором.
        request_timeout_ms=70000,           # Максимальное время ожидания ответа от Kafka. Если ответа нет → ошибка.
        reconnect_backoff_ms=5000,           # Если соединение потеряно: Producer будет ждать 5 секунд перед переподключением.
        reconnect_backoff_max_ms=10000,     # Максимальная задержка между reconnect попытками.

    )

    producer.send('register-events', message)
    producer.close()

    for _ in range(5):
        response = mail.find_message(query=login)
        if response.json()["total"] > 0:
            break
        time.sleep(1)
    else:
        raise AssertionError("Mail not found")
