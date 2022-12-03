from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError

from account.decorators import authenticated

from .models import ConnectionRequest



@api_view(['POST'])
@authenticated
def send_connection_request(req, user_id, *args, **kwargs):
    try:
        if req.user.id == user_id: return Response({'message': 'can NOT connect with same lister'}, status=status.HTTP_400_BAD_REQUEST)
        if ConnectionRequest.objects.filter(sender_id=user_id, receiver_id=req.user.id).exists():
            return Response({'message': 'connection request exists'}, status=status.HTTP_400_BAD_REQUEST)
        ConnectionRequest.objects.create(sender_id=req.user.id, receiver_id=user_id)
        return Response(status=status.HTTP_200_OK)
    except IntegrityError as e:
        print(e.args[0])
        return Response({'message': 'integrity error'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def accept_connection_request(req, user_id, *args, **kwargs):
    try:
        connection_request = ConnectionRequest.objects.get(sender_id=user_id, receiver=req.user.id)
        
    except:
        pass