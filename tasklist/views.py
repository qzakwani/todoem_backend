from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from account.decorators import authenticated
from core.exceptions import MissingInput, NotConnectedLister
from core.pagination import paginate_list
from lister.models import ConnectedListers


from .serializers import CreateSentTaskListSerializer, ReadSentTaskListSerializer
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
    except Exception as e:
        return Response({'message': "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)