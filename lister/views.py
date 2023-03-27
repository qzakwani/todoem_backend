from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.db.models import Q


from core.pagination import paginate_list
from account.decorators import authenticated
from account.models import User


from .models import ConnectionRequest, ConnectedLister
from .serializers import ConnectionRequestSerializer, ConnectedListerSerializer, ListerSerializer
from .exceptions import SearchInvalid
from .utils import check_connection_status, is_lister


#########################
## Connection Requests ##
#########################
@api_view(['POST'])
@authenticated
def send_connection_request(req, user_id, *args, **kwargs):
    try:
        if req.user.id == user_id: 
            return Response({'message': 'can NOT connect with yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(id=user_id, private=True).exists():
            return Response({'message': 'lister is private'}, status=status.HTTP_400_BAD_REQUEST)
        
        if ConnectionRequest.objects.filter(sender_id=user_id, receiver_id=req.user.id).exists():
            return Response({'message': 'lister already sent a request to you'}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_lister(req.user.id, user_id):
            return Response({'message':  'lister connected already'}, status=status.HTTP_400_BAD_REQUEST)
        
        ConnectionRequest.objects.create(sender_id=req.user.id, receiver_id=user_id)
        
        return Response(status=status.HTTP_200_OK)
    except (ValidationError, IntegrityError):
        return Response({'message':  'request has already been sent'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def accept_connection_request(req, user_id, *args, **kwargs):
    try:
        i, _ = ConnectionRequest.objects.filter(sender_id=user_id, receiver_id=req.user.id).delete()
        if i != 1:
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        ConnectedLister.objects.bulk_create([
            ConnectedLister(user_id=user_id, lister_id=req.user.id),
            ConnectedLister(user_id=req.user.id, lister_id=user_id)
        ])
        return Response(status=status.HTTP_200_OK)
    except (ValidationError, IntegrityError):
        return Response({'message':  'lister connected already'}, status=status.HTTP_400_BAD_REQUEST)
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
        requests = ConnectionRequest.objects.filter(receiver_id=req.user.id).order_by('-sent_at').select_related('sender')
        page_number = req.query_params.get('page', 1)
        page = paginate_list(requests, 10, page_number)
        ser = ConnectionRequestSerializer(page, many=True)
        return Response({'next': page.has_next(), 'requests': ser.data}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



##############
##  STATUS  ##
##############
@api_view(['GET'])
@authenticated
def connection_status(req, lister_id, *args, **kwargs):
    try:
        if req.user.id == lister_id:
            raise
        return Response({'status': check_connection_status(req.user.id, lister_id).value}, status=status.HTTP_200_OK)
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
        listers = ConnectedLister.objects.filter(user_id=req.user.id).select_related('lister').order_by('-date_connected')
        page = paginate_list(listers, 100, page_number)
        ser = ConnectedListerSerializer(page, many=True)
        return Response({'next': page.has_next(), 'listers': ser.data}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_lister(req, lister_id, *args, **kwargs):
    try:
        lister = User.objects.get(id=lister_id)
        ser = ListerSerializer(lister)
        return Response(ser.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authenticated
def get_lister_by_username(req, username, *args, **kwargs):
    try:
        lister = User.objects.get(username=username)
        ser = ListerSerializer(lister)
        return Response(ser.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
def disconnect_lister(req, lister_id, *args, **kwargs):
    try:
        i, _ = ConnectedLister.objects.filter(user=req.user.id, lister=lister_id).delete()
        j, _ = ConnectedLister.objects.filter(user=lister_id, lister=req.user.id).delete()
        if i == 0 or j == 0:
            raise ObjectDoesNotExist()
        return Response(status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@authenticated
def search_my_listers(req, *args, **kwargs):
    try:
        page_number = req.query_params.get('page', 1)
        search = req.data.get('search', None)
        if search is None: raise SearchInvalid('empty search')
        query = ConnectedLister.objects.filter(Q(user_id=req.user.id), Q(lister__username__icontains=search) | Q(lister__name__icontains=search)).select_related('lister')
        page = paginate_list(query, 5, page_number)
        ser = ConnectedListerSerializer(page, many=True)
        return Response({'next': page.has_next(), 'result': ser.data}, status=status.HTTP_200_OK)
    except SearchInvalid as e:
        return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
@authenticated
def search_listers(req, *args, **kwargs):
    try:
        page_number = req.query_params.get('page', 1)
        search = req.data.get('search', None)
        if search is None: raise SearchInvalid('empty search')
        query = User.objects.filter(Q(private=False), Q(username__icontains=search) | Q(name__icontains=search)).exclude(id=req.user.id).only('id', 'username', 'name')
        page = paginate_list(query, 10, page_number)
        ser = ListerSerializer(page, many=True)
        return Response({'next': page.has_next(), 'result': ser.data}, status=status.HTTP_200_OK)
    except SearchInvalid as e:
        return Response({'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


