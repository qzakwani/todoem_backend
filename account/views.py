from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from .serializers import UserSerializer
from .decorators import authenticated, reauthenticate

@api_view(['POST'])
def sign_up(req):
    ser = UserSerializer(data=req.POST)
    if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authenticated
@reauthenticate
def try_me(req, u):
    print('here')
    return Response({'hello': f'{u.username}'})