from celery import shared_task


@shared_task
def lol():
    return 8