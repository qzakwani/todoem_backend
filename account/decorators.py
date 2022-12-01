from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .models import User
from .exceptions import MissingInput, InvalidPassword


def authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return Response({'message': 'not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper_func


def reauthenticate(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            password = request.POST.get('password', None)
            if password is None: raise MissingInput('password missing')
            if not user.check_password(password): raise InvalidPassword('invalid password')
            return view_func(request, user, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        except (MissingInput, InvalidPassword) as e:
            return Response({'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper_func