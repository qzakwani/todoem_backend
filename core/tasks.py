from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery.utils.log import get_task_logger
from anymail.exceptions import AnymailError


logger = get_task_logger(__name__)

@shared_task(ignore_result=True)
def send_todoem_email(
    name: str,
    from_username: str, 
    to: list[str], 
    subj: str, 
    template: str, 
    ctx: dict = None):
    
    _from = f"{name} <{from_username}{settings.MAIN_EMAIL_DOMAIN}>"
    try:
        msg = render_to_string(template, context=ctx)
        send_mail(
            subject=subj,
            message=msg,
            from_email=_from,
            recipient_list=to,
            fail_silently=False
        )
    except AnymailError as err:
        logger.error(err)
    except Exception as e:
        logger.error(
            f'''
            Exception: {type(e)},
            
            args: {e.args}
        '''
        )
