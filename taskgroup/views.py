from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from account.decorators import authenticated
from lister.models import ConnectedListers
from core.exceptions import NotConnectedLister

from .serializers import TaskGroupSerializer
from .models import TaskGroup
from .exceptions import MembersError


@api_view(['POST'])
@authenticated
def create_taskgroup(req, *args, **kwargs):
    try:
        ser = TaskGroupSerializer(data=req.data)
        users = req.data.get('members', None)
        if users is None or len(users) > 20 or not isinstance(users, list):
            raise MembersError('exceeds 20 or not provided or wrong format')
        
        U = get_user_model()
        members  = [U.objects.get(id=req.user.id)]
        for user in users:
            u = U.objects.get(id=user)
            if ConnectedListers.objects.filter(user_id=req.user.id, listers=u).exists():
                members.append(u)
            else:
                raise NotConnectedLister('not connected lister')
        
        if ser.is_valid():
            taskgroup = ser.save(admin_id=req.user.id)
            taskgroup.members.add(*members)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    except (MembersError, NotConnectedLister) as err:
        return Response({'message': err.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as rr:
        print(type(rr))
        return Response({'message': rr.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authenticated
def delete_taskgroup(req, taskgroup_id, *args, **kwargs):
    try:
        i, _ = TaskGroup.objects.filter(id=taskgroup_id, admin_id=req.user.id).delete()
        if i == 0:
            raise ObjectDoesNotExist()
        return Response(status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        return Response({'message': 'taskgroup not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@authenticated
def update_taskgroup(req, taskgroup_id,*args, **kwargs):
    try:
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, admin_id=req.user.id)
        ser = TaskGroupSerializer(instance=taskgroup, data=req.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'message': 'taskgroup not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authenticated
def my_taskgroup(req,*args, **kwargs):
    try:
        taskgroups = TaskGroup.objects.filter(admin_id=req.user.id)
        ser = TaskGroupSerializer(taskgroups, many=True)
        return Response(ser.data)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authenticated
def list_taskgroup(req,*args, **kwargs):
    try:
        taskgroups = TaskGroup.objects.filter(members=req.user.id)
        ser = TaskGroupSerializer(taskgroups, many=True)
        return Response(ser.data)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Admin Action
@api_view(['POST'])
@authenticated
def add_member(req, taskgroup_id, member_id, *args, **kwargs):
    try:
        if req.user.id == member_id: raise
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, admin_id=req.user.id)
        
        U = get_user_model()
        member = U.objects.get(id=member_id)
        if not ConnectedListers.objects.filter(user_id=req.user.id, listers=member).exists():
            raise NotConnectedLister()
        
        taskgroup.members.add(member)
        return Response(status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        return Response({'message': 'user or taskgroup not found'}, status=status.HTTP_404_NOT_FOUND)
    except NotConnectedLister:
        return Response({'message': 'not connected lister'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def kick_member(req, taskgroup_id, member_id, *args, **kwargs):
    try:
        if req.user.id == member_id: raise
        taskgroup = TaskGroup.objects.get(id=taskgroup_id, admin_id=req.user.id)
        
        U = get_user_model()
        member = U.objects.get(id=member_id)
        
        taskgroup.members.remove(member)
        return Response(status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist:
        return Response({'message': 'user or taskgroup not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from django.shortcuts import render
def testo(req, *args, **kwargs):
    return render(req, 'testo.html')