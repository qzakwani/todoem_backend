from rest_framework.response import Response
from rest_framework import status

def authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return Response({'message': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper_func