from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from lister.models import ConnectedLister

from .serializers import TaskGroupTaskSerializer
from .models import TaskGroupTask, TaskGroup, TaskGroupMember


'''
** request and response **

    -- content --
{
    action: create | delete | edit | complete | error | kick | add | change | terminate | leave
    target: None | id
    data: None | dict{}
    msg: None | str -> if error
} 

** group communication **

    -- event --

{
    type: str[method name with '.' to '_']
    content: None | dict{}
}

'''


class TaskGroupConsumer(AsyncJsonWebsocketConsumer):
    taskgroup_db = None
    uid = None
    member = None
    taskgroup = None
    
    async def initialize(self):
        try:
            self.taskgroup_id = self.scope["url_route"]["kwargs"]["taskgroup_id"]
            self.uid = self.scope['user'].id
            
            self.member = await TaskGroupMember.objects.aget(taskgroup_id=self.taskgroup_id, member_id=self.uid)
            
            if self.member is not None:
                self.taskgroup_db = str(self.taskgroup_id)
                return True
            else:
                return False
        except ObjectDoesNotExist:
                await self.accept()
                await self.send_json({'action': 'error', 'msg': 'you are not part of this group'})
                await self.close(1000)
        except:
            return False
    
    async def connect(self):
        if await self.initialize():
            # Join room group
            await self.channel_layer.group_add(self.taskgroup_db, self.channel_name)
            
            await self.accept()
        else:
            await self.accept()
            await self.close(1011)

    async def disconnect(self, close_code):
        if self.taskgroup_db is not None:
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
            case 'edit':
                await self.edit_task(content)
            case 'change':
                await self.change_perms(content)
            case 'add':
                await self.add_memeber(content)
            case 'kick':
                await self.kick_member(content)
            
            case _:
                await self.send_json({'action': 'error', 'msg': 'action invalid or missing'})
    
    
    ## * permissions * ##
    async def admin(self):
        if self.member.is_admin:
            return True
        else:
            await self.send_json({'action': 'error', 'msg': 'Unauthorized admin action'})
            return False
    
    async def staff(self):
        if self.member.is_staff:
            return True
        else:
            await self.send_json({'action': 'error', 'msg': 'Unauthorized staff action'})
            return False
    
    ## * helpers * ##
    async def fetch_taskgroup(self):
        if self.taskgroup is None:
            self.taskgroup = await TaskGroup.objects.aget(id=self.taskgroup_id)
            return self.taskgroup
        else:
            self.taskgroup
    

    ## * creator or admin actions * ## 
    async def terminate(self):
        try:
            if await self.admin():
                i, _ = await TaskGroup.objects.adelete(id=self.taskgroup_id)
                if i == 0:
                    await self.send_json({'action': 'error', 'msg': 'termination failed'})
                    return
                else:
                    await self.channel_layer.group_send(self.taskgroup_db, {'type': 'close'})
        except:
            await self.close(1013)

    
    ## * admin actions * ##
    async def add_memeber(self, content):
        try:
            member_id = content.get('target', None)
            if member_id is None:
                await self.send_json({'action': 'error', 'msg': 'lister not provided'})
            #todo
        except ValidationError as err:
            await self.send_json({'action': 'error', 'msg': err.args[0]})
        except:
            await self.send_json({'action': 'error', 'msg': 'addtion failed'})
    
    async def kick_memeber(self, content):
        pass
    
    async def change_perms(self, content):
        pass



    ## * staff actions * ##
    async def create_task(self, content):
        if await self.staff():
            data = content.get('data', None)
            ser = TaskGroupTaskSerializer(data=data)
            if ser.is_valid():
                task = await TaskGroupTask.objects.acreate(taskgroup_id=self.taskgroup_id, created_by_id=self.uid, **ser.validated_data)

                await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': TaskGroupTaskSerializer(task).data})
                
            else:
                await self.send_json({'action': 'error', 'msg': ser.errors})


    async def delete_task(self, content):
        if await self.staff():
        
            task_id = content.get('target', None)
        
            if task_id is None:
                return await self.send_json({'action': 'error', 'msg': 'task id is not provided'})
            else:
                i, _ = await TaskGroupTask.objects.filter(id=task_id, taskgroup_id=self.taskgroup_id).adelete()
                if i != 1:
                    return await self.send_json({'action': 'error', 'msg': 'deletion failed'})
                else:
                    await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': {'action': 'delete', 'target': task_id}})


    async def edit_task(self, content):
        pass

    
    
    ## * member actions * ##
    async def complete_task(self, content):
        comment = content.get('comment', None)
        task_id = content.get('target', None)
        
        if task_id is None:
            return await self.send_json({'action': 'error', 'msg': 'task id is not provided'})
        else:
            i = await TaskGroupTask.objects.filter(id=task_id, taskgroup_id=self.taskgroup_id, completed=False).aupdate(completed=True, comment=comment, completed_by_id=self.uid)
            
            if i != 1:
                return await self.send_json({'action': 'error', 'msg': 'deletion failed'})
            else:
                task = await TaskGroupTask.objects.aget(id=task_id)
                await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': {'action': 'complete', 'target': task_id, 'data': TaskGroupTaskSerializer(task).data}})




    ## * group actions * ##
    async def send_response(self, event):
        await self.send_json(event['content'])
