# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
# from .redis_db import r_db

__all__ = ('celery_app',)