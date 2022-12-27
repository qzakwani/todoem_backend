import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


from .serializers import TaskGroupTaskSerializer
from .models import TaskGroupTask

class TaskGroupConsumer(AsyncJsonWebsocketConsumer):
    
    uid = None
    is_admin = False
    
    async def connect(self):
        import random
        
        self.uid=random.randint(1, 99)
        
        self.taskgroup_id = self.scope["url_route"]["kwargs"]["taskgroup_id"]
        self.taskgroup_db = self.taskgroup_id

        # Join room group
        await self.channel_layer.group_add(self.taskgroup_db, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.taskgroup_db, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content):
        action = content.get('action', None)
        match action:
            case 'create':
                await self.create_task(content)
            case 'complete':
                await self.complete_task(content)
            case 'delete':
                await self.delete_task(content)
            case _:
                await self.send_json({'action': 'error', 'msg': 'action invalid or missing'})
    
    
    async def create_task(self, content):
        data = content.get('data', None)
        ser = TaskGroupTaskSerializer(data=data)
        if ser.is_valid():
            task = await TaskGroupTask.objects.acreate(taskgroup_id=self.taskgroup_id, **ser.validated_data)

            await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': TaskGroupTaskSerializer(task).data})
            
        else:
            await self.send_json({'action': 'error', 'msg': ser.errors})



    async def delete_task(self, content):
        task_id = content.get('target', None)
        
        if task_id is None:
            await self.send_json({'action': 'error', 'msg': 'task id is not provided'})
            return
        
        i, _ = await TaskGroupTask.objects.filter(id=task_id, taskgroup_id=self.taskgroup_id).adelete()
        if i != 1:
            await self.send_json({'action': 'error', 'msg': ''})
            return
        await self.send_json({'action': 'delete', 'target': task_id})
    



    async def complete_task(self, content):
        comment = content.get('comment', None)
        task_id = content.get('target', None)
        
        if task_id is None:
            await self.send_json({'action': 'error', 'msg': 'task id is not provided'})
            return
        
        i = await TaskGroupTask.objects.filter(id=task_id, taskgroup_id=self.taskgroup_id, completed=False).aupdate(completed=True, comment=comment, completed_by_id=self.uid)
        
        if i != 1:
            await self.send_json({'action': 'error', 'msg': ''})
            return
        
        task = await TaskGroupTask.objects.aget(id=task_id)
        await self.send_json({'action': 'complete', 'target': task_id, 'data': TaskGroupTaskSerializer(task).data})


    async def send_response(self, event):
        await self.send_json(event['content'])