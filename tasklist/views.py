from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist


from account.decorators import authenticated
from core.exceptions import MissingInput, NotConnectedLister, DeleteFailed, UpdateFailed
from core.pagination import paginate_list
from lister.models import ConnectedListers


from .serializers import CreateSentTaskListSerializer, ReadSentTaskListSerializer, SentTaskListTaskSerializer, TaskListSerializer, TaskListTaskSerializer
from .tasks import send_tasklist
from .models import SentTaskList, SentTaskListTask, TaskList, TaskListTask


################
#*    SENT    *#
################
@api_view(['POST'])
@authenticated
def create_tasklist(req, *args, **kwargs):
    try:
        _to = req.data.get('to', None)
        if _to is None: raise MissingInput('to: missing')
        
        if not ConnectedListers.objects.filter(user_id=req.user.id, listers__id=_to).exists():
            raise NotConnectedLister('to: not connected lister')
        
        ser = CreateSentTaskListSerializer(data=req.data)
        
        if ser.is_valid():
            task_list = ser.save(sender_id=req.user.id, receiver_id=_to)
            send_tasklist.delay(task_list.id, req.user.id, _to, ser.validated_data)
    
            return Response(ReadSentTaskListSerializer(task_list).data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def list_sent_tasklist(req, *args, **kwargs):
    try:
        page_number = req.query_params.get('page', 1)
        tasklist = SentTaskList.objects.filter(sender_id=req.user.id)
        page = paginate_list(tasklist, 20, page_number)
        ser = ReadSentTaskListSerializer(page, many=True)
        return Response({'next': page.has_next(), 'tasklists': ser.data}, status=status.HTTP_200_OK)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_sent_tasklist_tasks(req, list_id, *args, **kwargs):
    try:
        _list = SentTaskList.objects.get(id=list_id, sender_id=req.user.id)
        tasks = SentTaskListTask.objects.filter(tasklist=_list)
        return Response(SentTaskListTaskSerializer(tasks, many=True).data)
    except ObjectDoesNotExist:
        return Response({'message': 'tasklist not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authenticated
def delete_sent_tasklist(req, list_id, *args, **kwargs):
    try:
        i, _ = SentTaskList.objects.filter(id=list_id, sender_id=req.user.id).delete()
        if i == 0: raise DeleteFailed()
        return Response(status=status.HTTP_200_OK)
    except DeleteFailed:
        return Response({'message': 'deletion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



####################
#*    RECEIVED    *#
####################
@api_view(['GET'])
@authenticated
def list_tasklist(req, *args, **kwargs):
    try:
        page_number = req.query_params.get('page', 1)
        tasklist = TaskList.objects.filter(receiver_id=1)
        page = paginate_list(tasklist, 20, page_number)
        ser = TaskListSerializer(page, many=True)
        return Response({'next': page.has_next(), 'tasklists': ser.data}, status=status.HTTP_200_OK)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authenticated
def get_tasklist_tasks(req, list_id, *args, **kwargs):
    try:
        _list = TaskList.objects.get(id=list_id, receiver_id=1)
        tasks = TaskListTask.objects.filter(tasklist=_list)
        return Response(TaskListTaskSerializer(tasks, many=True).data)
    except ObjectDoesNotExist:
        return Response({'message': 'tasklist not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['DELETE'])
@authenticated
def delete_tasklist(req, list_id, *args, **kwargs):
    try:
        i, _ = TaskList.objects.filter(id=list_id, receiver_id=1).delete()
        if i == 0: raise DeleteFailed()
        return Response(status=status.HTTP_200_OK)
    except DeleteFailed:
        return Response({'message': 'deletion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def complete_tasklist(req, list_id, *args, **kwargs):
    try:
        i = TaskList.objects.filter(id=list_id, receiver_id=req.user.id).update(completed=True)
        if i != 1: raise UpdateFailed()
        return Response(status=status.HTTP_200_OK)
    except UpdateFailed:
        return Response({'message': 'update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def complete_tasklist_task(req, list_id, task_id, *args, **kwargs):
    try:
        i = TaskListTask.objects.filter(id=task_id, tasklist_id=list_id, tasklist__receiver_id=req.user.id).update(completed=True)
        if i != 1: raise UpdateFailed()
        return Response(status=status.HTTP_200_OK)
    except UpdateFailed:
        return Response({'message': 'update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def uncomplete_tasklist(req, list_id, *args, **kwargs):
    try:
        i = TaskList.objects.filter(id=list_id, receiver_id=req.user.id).update(completed=False)
        if i != 1: raise UpdateFailed()
        return Response(status=status.HTTP_200_OK)
    except UpdateFailed:
        return Response({'message': 'update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def uncomplete_tasklist_task(req, list_id, task_id, *args, **kwargs):
    try:
        i = TaskListTask.objects.filter(id=task_id, tasklist_id=list_id, tasklist__receiver_id=req.user.id).update(completed=False)
        if i != 1: raise UpdateFailed()
        return Response(status=status.HTTP_200_OK)
    except UpdateFailed:
        return Response({'message': 'update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)