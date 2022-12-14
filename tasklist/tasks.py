from celery import shared_task
from celery.utils.log import get_task_logger


from core.exceptions import UpdateFailed


from .models import TaskList, TaskListTask, SentTaskList
from .utils import insert_tasklist


logger = get_task_logger(__name__)


@shared_task(ignore_result=True)
def send_tasklist(id: int, sender: int, receiver: int, data: dict):
    try:
        insert_tasklist(TaskList, TaskListTask, {"id": id, "sender_id": sender, "receiver_id": receiver, **data})
        
        i = SentTaskList.objects.filter(id=id).update(delivered=True)
        
        if i != 1:
            raise UpdateFailed('delivered: not updated')
    except Exception as e:
        logger.error(
        f'''
            tasklist: {id},
            
            Exception: {type(e)},
            
            args: {e.args}
        '''
        )