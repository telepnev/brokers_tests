import pytest
from kafka import KafkaProducer

from framework.internal.http.account import AccountApi
from framework.internal.http.mail import MailApi
from framework.internal.kafka.produscer import Producer


@pytest.fixture(scope="session")
def account() -> AccountApi:
    return AccountApi()

@pytest.fixture(scope="session")
def mail() -> MailApi:
    return MailApi()


@pytest.fixture(scope="session")
def kafka_producer() -> Producer:
    with Producer() as producer:
        yield producer