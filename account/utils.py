from core.encryption import TodoemEncryption
from core.tasks import send_todoem_email


def send_verification_email(email: str, base_link: str):
    try:
        enc = TodoemEncryption(data=email)
        send_todoem_email.delay(
            "todoem",
            "verify-email",
            [email,],
            "Verify todoem Email",
            "verify_email.txt",
            ctx={"link": f"{base_link}{enc.encrypt()}/"}
        )
        return
    except Exception as e:
        raise e
    