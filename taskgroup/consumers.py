from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from lister.utils import ais_lister

from .serializers import TaskGroupTaskSerializer, TaskGroupMemberSerializer
from .models import TaskGroupTask, TaskGroup, TaskGroupMember


'''
** request and response **

    -- content --
{
    action: create | delete | edit | complete | error | kick | add | change | terminate | leave
    target: None | id
    data: None | dict{}
    msg: None | str -> if error
    pos: None | if change -> str[admin | staff | member]
} 

** group communication **

    -- event --

{
    type: str[method name with '.' to '_']
    content: None | dict{}
}

'''

User = get_user_model()

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
        except TaskGroupMember.DoesNotExist:
                await self.accept()
                await self.send_json({'action': 'error', 'msg': 'you are not part of this group'})
                await self.close()
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
                await self.add_member(content)
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
        if self.member.is_staff or self.member.is_admin:
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
        if await self.admin():
            i, _ = await TaskGroup.objects.adelete(id=self.taskgroup_id)
            if i == 0:
                await self.send_json({'action': 'error', 'msg': 'termination failed'})
                return
            else:
                await self.channel_layer.group_send(self.taskgroup_db, {'type': 'close'})


    
    ## * admin actions * ##
    async def add_member(self, content):
        if await self.admin():
            try:
                member_id = content.get('target', None)
                if member_id is None:
                    await self.send_json({'action': 'error', 'msg': 'lister not provided'})
                    return
                if await ais_lister(self.uid, member_id):
                    user = await User.objects.aget(id=member_id)
                    member = await TaskGroupMember.objects.acreate(taskgroup_id=self.taskgroup_id, member=user)
                    await self.channel_layer.group_send(self.taskgroup_db, 
                                                        {'type': 'send_response',
                                                         'content': {
                                                             'action': 'add',
                                                             'data': TaskGroupMemberSerializer(member, 
                                                                                               context={'member': user}).data}})
                else:
                    await self.send_json({'action': 'error', 'msg': 'lister not connected'})
                    return
            except IntegrityError:
                await self.send_json({'action': 'error', 'msg': 'lister already added'})
            except User.DoesNotExist:
                await self.send_json({'action': 'error', 'msg': 'lister not found'})
            except:
                await self.send_json({'action': 'error', 'msg': 'addtion failed'})
    
    async def kick_member(self, content):
        if await self.admin():
            try:
                member_id = content.get('target', None)
                if member_id is None:
                    await self.send_json({'action': 'error', 'msg': 'lister not provided'})
                    return
                
                i, _ = await TaskGroupMember.objects.filter(taskgroup_id=self.taskgroup_id, member_id=member_id).adelete()
                
                if i == 0:
                    raise
                
                await self.channel_layer.group_send(self.taskgroup_db, 
                                                    {'type': 'handel_kick',
                                                        'content': content
                                                        }
                                                    )
            except:
                await self.send_json({'action': 'error', 'msg': 'deletion failed'})
    
    async def change_perms(self, content):
        if await self.admin():
            try:
                member_id = content.get('target', None)
                pos = content.get('pos', None)
                if member_id is None or pos is None:
                    await self.send_json({'action': 'error', 'msg': 'lister or position not provided'})
                    return
                if pos not in ['admin', 'staff', 'member']:
                    await self.send_json({'action': 'error', 'msg': 'invalid position'})
                    return 
                
                i = await TaskGroupMember.objects.filter(taskgroup_id=self.taskgroup_id, member_id=member_id).aupdate(is_admin=(pos=='admin'), is_staff=(pos=='staff'))
                
                if i == 0:
                    raise
                
                await self.channel_layer.group_send(self.taskgroup_db, 
                                                    {'type': 'send_response',
                                                        'content': content
                                                        }
                                                    )
            except:
                await self.send_json({'action': 'error', 'msg': 'change failed'})



    ## * staff actions * ##
    async def create_task(self, content):
        if await self.staff():
            try:
                data = content.get('data', None)
                ser = TaskGroupTaskSerializer(data=data)
                if ser.is_valid():
                    task = await TaskGroupTask.objects.acreate(taskgroup_id=self.taskgroup_id, created_by_id=self.uid, **ser.validated_data)

                    await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': {
                        'action': 'create',
                        'data': TaskGroupTaskSerializer(task).data}
                    })
                    
                else:
                    await self.send_json({'action': 'error', 'msg': ser.errors})
            except:
                await self.send_json({'action': 'error', 'msg': 'creation failed'})

    async def delete_task(self, content):
        if await self.staff():
            try:
                task_id = content.get('target', None)
            
                if task_id is None:
                    await self.send_json({'action': 'error', 'msg': 'task id is not provided'})
                    return
                else:
                    i, _ = await TaskGroupTask.objects.filter(id=task_id, taskgroup_id=self.taskgroup_id).adelete()
                    if i != 1:
                        return await self.send_json({'action': 'error', 'msg': 'task not found'})
                    else:
                        await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': {'action': 'delete', 'target': task_id, 'by': self.uid}})
            except:
                await self.send_json({'action': 'error', 'msg': 'deletion failed'})


    async def edit_task(self, content):
        if await self.staff():
            try:
                task_id = content.get('target', None)
                if task_id is None:
                    await self.send_json({'action': 'error', 'msg': 'task id is not provided'})
                    return
                
                data = content.get('data', None)
                ser = TaskGroupTaskSerializer(data=data)
                
                if ser.is_valid():
        
                    i = await TaskGroupTask.objects.filter(id=task_id, taskgroup_id=self.taskgroup_id).aupdate(edited=True, **ser.validated_data)
                    
                    if i == 0:
                        await self.send_json({'action': 'error', 'msg': 'task not found'})
                        return
                    
                    await self.channel_layer.group_send(self.taskgroup_db, {'type': 'send_response', 'content': {'action': 'delete', 'target': task_id, 'data': ser.data}})
                    
                else:
                    await self.send_json({'action': 'error', 'msg': ser.errors})
            except Exception as e:
                print(type(e))
                print(e.args)
                await self.send_json({'action': 'error', 'msg': 'edit failed'})

#todo HERE
    
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
        
    
    
    async def handel_kick(self, event):
        id = event['content']['target']
        await self.send_json(event['content'])    
        if int(id) == self.uid:
            await self.close()
        

