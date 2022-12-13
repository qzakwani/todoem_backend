from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from account.decorators import authenticated
from core.exceptions import MissingInput, NotConnectedLister
from lister.models import ConnectedListers


from .serializers import TaskListSerializer, TaskListTaskSerializer


@api_view(['POST'])
@authenticated
def create_tasklist(req, *args, **kwargs):
    try:
        _to = req.data.get('to', None)
        if _to is None: raise MissingInput('to: missing')
        if ConnectedListers.listers.through.objects.filter(connectedlisters_id=req.user.id, user_id=_to).exists():
            raise NotConnectedLister('to: not connected lister')
        
        ser = TaskListSerializer(req.data)
        
        if ser.is_valid():
            ser.save(sender_id=req.user.id, receiver_id=_to)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        return Response(status=status.HTTP_200_OK)
    except:
        pass
    
