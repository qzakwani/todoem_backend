from core.encryption import TodoemEncryption, TodoemTokenError
from core.tasks import send_todoem_email
from core.dt import TodoemDT

from .models import User


def generate_email_token(user: User, action: str, expire=True) -> str:
    """
    Generates an encrypted email token for the specified user and action.
    
    Args:
        user: The user to generate the token for.
        action: The action that the token is being generated for.
        expire (optional): A flag indicating whether the token should expire. Default is True.
        
    Returns:
        The encrypted email token.
    """
    return TodoemEncryption.encrypt_dict(
        {
            'action': action,
            'email': user.email,
            'signature': TodoemDT.datetime_to_str(user.last_modified)
        },
        expire=expire
    )

def validate_email_token(token: str, action: str) -> User:
    """
    Validates an email token and returns the user it is associated with.
    
    Args:
        token: The email token to validate.
        action: The action that the token is expected to be for.
        
    Returns:
        The user associated with the token.
        
    Raises:
        TodoemTokenError: If the token is invalid or has expired, or if the action does not match the expected action.
    """
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
    """
    Sends a verification email to the specified user with a link to verify their email address.
    
    Args:
        user: The user to send the email to.
        base_link: The base URL for the application.
        
    Returns:
        None
    
    Raises:
        Exception: If an error occurs while sending the email or generating the email token.
    """
    try:
        token = generate_email_token(user, 'verify-email')
        send_todoem_email.delay(
            "todoem",
            "verify-email",
            [user.email,],
            "Verify todoem Email",
            "verify_email.txt",
            ctx={"link": f"{base_link}/account/verify-email/{token}/",
                 "username": user.display_name}
        )
        return
    except Exception as e:
        raise e


def send_reset_password_email(user: User, base_link: str):
    """
    Sends a forgot password email to the specified user with a link to verify their email address.
    
    Args:
        user: The user to send the email to.
        base_link: The base URL for the application.
        
    Returns:
        None
    
    Raises:
        Exception: If an error occurs while sending the email or generating the email token.
    """
    try:
        token = generate_email_token(user, 'forgot-password')
        send_todoem_email.delay(
            "todoem",
            "forgot-password",
            [user.email,],
            "Forgot todoem Password",
            "reset_password_email.txt",
            ctx={"link": f"{base_link}/account/forgot-password/{token}/",
                 "name": user.display_name}
        )
        return
    except Exception as e:
        raise e