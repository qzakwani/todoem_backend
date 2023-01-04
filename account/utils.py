from core.encryption import TodoemEncryption, TodoemTokenError
from core.tasks import send_todoem_email
from core.dt import TodoemDT

from .models import User

def get_base_url(request) -> str:
    return f"{request.scheme}://{request.get_host()}"


def generate_email_token(user: User, action: str, expire=True) -> str:
    return TodoemEncryption.encrypt_dict(
        {
            'action': action,
            'email': user.email,
            'signature': TodoemDT.datetime_to_str(user.last_modified)
        },
        expire=expire
    )

def validate_email_token(token: str, action: str) -> User:
    data, valid = TodoemEncryption.decrypt_dict(token)
    if not valid:
        raise TodoemTokenError('expired link')
    if data['action'] != action:
        raise TodoemTokenError(f'invalid link for the action: {action}')
    try:
        user = User.objects.get(email=data['email'])
        if not TodoemDT.compare(data['signature'], '=', user.last_modified):
            raise TodoemTokenError('link is already used once')
        return user
    except User.DoesNotExist:
        raise TodoemTokenError(f'account ({data["email"]}) not found')
    

def send_verification_email(user: User, base_link: str):
    try:
        token = generate_email_token(user, 'verify-email')
        send_todoem_email.delay(
            "todoem",
            "verify-email",
            [user.email,],
            "Verify todoem Email",
            "verify_email.txt",
            ctx={"link": f"{base_link}/account/verify-email/{token}/",
                 "name": user.display_name}
        )
        return
    except Exception as e:
        raise e


def send_reset_password_email(user: User, base_link: str):
    try:
        token = generate_email_token(user, 'forgot-password')
        send_todoem_email.delay(
            "todoem",
            "reset-password",
            [user.email,],
            "Reset todoem Password",
            "reset_password_email.txt",
            ctx={"link": f"{base_link}/account/reset-password/{token}/",
                 "name": user.display_name}
        )
        return
    except Exception as e:
        raise e