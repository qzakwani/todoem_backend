from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


from core.pagination import paginate_list
from account.decorators import authenticated
from account.models import User


from .models import ConnectionRequest, ConnectedListers
from .serializers import ConnectionRequestSerializer, ListerProfileSerializer
from .exceptions import SearchInvalid


#########################
## Connection Requests ##
#########################
@api_view(['POST'])
@authenticated
def send_connection_request(req, user_id, *args, **kwargs):
    try:
        if req.user.id == user_id: return Response({'message': 'can NOT connect with same lister'}, status=status.HTTP_400_BAD_REQUEST)
        if ConnectionRequest.objects.filter(sender_id=user_id, receiver_id=req.user.id).exists():
            return Response({'message': 'connection request exists'}, status=status.HTTP_400_BAD_REQUEST)
        ConnectionRequest.objects.create(sender_id=req.user.id, receiver_id=user_id)
        return Response(status=status.HTTP_200_OK)
    except IntegrityError:
        return Response({'message': 'integrity error'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def accept_connection_request(req, user_id, *args, **kwargs):
    try:
        '''
        could be improved by minimizing db hits
        '''
        connection_request = ConnectionRequest.objects.get(sender_id=user_id, receiver=req.user.id)
        ConnectedListers.objects.get(user=connection_request.sender).listers.add(connection_request.receiver)
        ConnectedListers.objects.get(user=connection_request.receiver).listers.add(connection_request.sender)
        connection_request.delete()
        return Response(status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@authenticated
def reject_connection_request(req, user_id, *args, **kwargs):
    try:
        ConnectionRequest.objects.filter(sender_id=user_id, receiver=req.user.id).delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def cancel_connection_request(req, lister_id, *args, **kwargs):
    try:
        ConnectionRequest.objects.filter(sender_id=req.user.id, receiver_id=lister_id).delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_connection_request(req, *args, **kwargs):
    try:
        requests = ConnectionRequest.objects.filter(receiver=req.user.id).order_by('sent_at')
        page_number = req.query_params.get('page', 1)
        page = paginate_list(requests, 10, page_number)
        ser = ConnectionRequestSerializer(page, many=True)
        return Response({'next': page.has_next(), 'listers': ser.data}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authenticated
def connection_status(req, lister_id, *args, **kwargs):
    try:
        connection_status = ConnectedListers.listers.through.objects.filter(connectedlisters_id=req.user.id, user_id=lister_id).exists()
        return Response({'status': connection_status}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#############
## Listers ##
#############
@api_view(['GET'])
@authenticated
def list_my_listers(req, *args, **kwargs):
    try:
        page_number = req.query_params.get('page', 1)
        listers = ConnectedListers.objects.get(user_id=req.user.id).listers.all()
        page = paginate_list(listers, 10, page_number)
        ser = ListerProfileSerializer(page, many=True)
        return Response({'next': page.has_next(), 'listers': ser.data}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def disconnect_lister(req, lister_id, *args, **kwargs):
    try:
        my_list = ConnectedListers.objects.select_related('user').get(user_id=req.user.id)
        lister_list = ConnectedListers.objects.select_related('user').get(user_id=lister_id)
        my_list.listers.remove(lister_list.user)
        lister_list.listers.remove(my_list.user)
        return Response(status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@authenticated
def search_listers(req, *args, **kwargs):
    try:
        page_number = req.query_params.get('page', 1)
        search = req.data.get('search', None)
        if search is None: raise SearchInvalid('empty search')
        query = User.objects.filter(username__icontains=search)
        page = paginate_list(query, 10, page_number)
        ser = ListerProfileSerializer(page, many=True)
        return Response({'next': page.has_next(), 'result': ser.data}, status=status.HTTP_200_OK)
    except SearchInvalid as e:
        return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


