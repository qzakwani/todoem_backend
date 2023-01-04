from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# from channels.layers import get_channel_layer

from account.decorators import authenticated
from lister.utils import is_lister
from core.exceptions import NotConnectedLister

from .serializers import TaskGroupSerializer, TaskGroupMemberSerializer, TaskGroupTaskSerializer
from .models import TaskGroup,TaskGroupMember, TaskGroupTask
from .exceptions import MembersError

# channel_layer = get_channel_layer()

@api_view(['POST'])
@authenticated
def create_taskgroup(req, *args, **kwargs):
    try:
        ser = TaskGroupSerializer(data=req.data)
        users = req.data.get('members', None)
        if users is None or not isinstance(users, list) or len(users) > 20:
            raise MembersError('members exceeds 20 or not provided or wrong format')
        
        if ser.is_valid():
            taskgroup = ser.save(creator_id=req.user.id)
            members = [TaskGroupMember(taskgroup=taskgroup, member_id=req.user.id)]
            for user in users:
                if is_lister(req.user.id, user):
                    members.append(TaskGroupMember(taskgroup=taskgroup, member_id=user))
                else:
                    taskgroup.delete()
                    raise NotConnectedLister(f'{user} is not a connected lister')
            TaskGroupMember.objects.bulk_create(members)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except (MembersError, NotConnectedLister) as err:
        return Response({'message': err.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#! dont work
# async def delete_taskgroup(req, taskgroup_id, *args, **kwargs):
#     try:
#         if req.user.is_authenticated:
#             i, _ = await TaskGroup.objects.filter(id=taskgroup_id, creator_id=req.user.id).adelete()
#             if i == 0:
#                 return Response({'message': 'taskgroup not found'}, status=status.HTTP_404_NOT_FOUND)
#             await channel_layer.group_send(str(taskgroup_id), {'type': 'close'})
#             return Response(status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response({'message': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#     except:
#         return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def update_taskgroup(req, taskgroup_id, *args, **kwargs):
    try:
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, creator_id=req.user.id)
        ser = TaskGroupSerializer(instance=taskgroup, data=req.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except TaskGroup.DoesNotExist:
        return Response({'message': 'taskgroup not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_taskgroup(req, taskgroup_id, *args, **kwargs):
    try:
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, members=req.user.id)
        ser = TaskGroupSerializer(taskgroup)
        return Response(ser.data)
    except TaskGroup.DoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def list_my_taskgroup(req,*args, **kwargs):
    try:
        taskgroups = TaskGroup.objects.filter(creator_id=req.user.id)
        ser = TaskGroupSerializer(taskgroups, many=True)
        return Response(ser.data)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authenticated
def list_all_taskgroup(req,*args, **kwargs):
    try:
        taskgroups = TaskGroup.objects.filter(members=req.user.id)
        ser = TaskGroupSerializer(taskgroups, many=True)
        return Response(ser.data)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_member(req, taskgroup_id, lister_id, *args, **kwargs):
    try:
        member = TaskGroupMember.objects.select_related('member').get(taskgroup_id=taskgroup_id, member_id=lister_id)
        return Response(TaskGroupMemberSerializer(member).data)
    except TaskGroupMember.DoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_all_members(req, taskgroup_id, *args, **kwargs):
    try:
        members = TaskGroupMember.objects.filter(taskgroup_id=taskgroup_id).select_related('member')
        return Response(TaskGroupMemberSerializer(members, many=True).data)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_task(req, taskgroup_id, task_id, *args, **kwargs):
    try:
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, members=req.user.id)
        task = TaskGroupTask.objects.get(id=task_id, taskgroup=taskgroup)
        return Response(TaskGroupTaskSerializer(task).data)
    except (TaskGroup.DoesNotExist, TaskGroupTask.DoesNotExist):
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_all_tasks(req, taskgroup_id, *args, **kwargs):
    try:
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, members=req.user.id)
        tasks = TaskGroupTask.objects.filter(taskgroup=taskgroup)
        return Response(TaskGroupTaskSerializer(tasks, many=True).data)
    except (TaskGroup.DoesNotExist):
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#* for websocket tests
# from django.shortcuts import render
# def testo(req, *args, **kwargs):
#     return render(req, 'testo.html')
