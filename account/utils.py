from core.encryption import TodoemEncryption
from core.tasks import send_todoem_email
from django.utils import timezone
from datetime import timedelta

EXPIRED_PERIOD = timedelta(days=3)


def get_base_url(request) -> str:
    return f"{request.scheme}://{request.get_host()}"

def dict_email_data(data: str) -> dict:
    """
    format: key1:|:value1;;key2:|:value2
    """
    result = {}
    statements = data.split(';;')
    for statement in statements:
        temp = statement.split(':|:')
        result[temp[0]] = temp[1]
    return result

def send_verification_email(email: str, base_link: str, user):
    try:
        enc = TodoemEncryption(data=f'action:|:verify-email;;email:|:{email}')
        send_todoem_email.delay(
            "todoem",
            "verify-email",
            [email,],
            "Verify todoem Email",
            "verify_email.txt",
            ctx={"link": f"{base_link}/account/verify-email/{enc.encrypt()}/",
                 "username": user.username}
        )
        return
    except Exception as e:
        raise e


def send_reset_password_email(email: str, base_link: str, user):
    try:
        enc = TodoemEncryption(data=f'action:|:reset-password;;email:|:{email}')
        send_todoem_email.delay(
            "todoem",
            "reset-password",
            [email,],
            "Reset todoem Password",
            "reset_password_email.txt",
            ctx={"link": f"{base_link}/account/reset-password/{enc.encrypt()}/",
                 "username": user.username}
        )
        return
    except Exception as e:
        raise e