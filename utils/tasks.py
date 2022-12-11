from celery import shared_task
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail


class BadEmail(Exception):
    pass

@shared_task
def send_todoem_email(
    _from: str = None, to: list[str] = None, template = None, context: dict = None
    ):
    _from = _from + settings.MAIN_EMAIL_DOMAIN
    try: 
        raise
    except:
        print('fail')