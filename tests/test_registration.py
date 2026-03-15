import time
import uuid

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
