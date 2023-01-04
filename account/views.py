from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.conf import settings

from core.encryption import TodoemEncryption

from .serializers import UserSerializer, LoginTokenSerializer, UpdateUserSerializer
from .decorators import authenticated, reauthenticate
from .exceptions import MissingInput, InvalidPassword
from .models import User
from .validators import validate_username 
from .utils import send_verification_email, get_base_url, send_reset_password_email, dict_email_data

@api_view(['POST'])
def sign_up(req, *args, **kwargs):
    ser = UserSerializer(data=req.data)
    if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = LoginTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        res.set_cookie(key="token", value=serializer.validated_data['access'], max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], httponly=True, samesite='Lax')
        return res

class RefreshLogin(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        res.set_cookie(key="token", value=serializer.validated_data['access'], max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], httponly=True, samesite='Lax')
        return res
        


@api_view(['GET'])
@authenticated
def get_user(req, *args, **kwargs):
    try:
        user = User.objects.get(id=req.user.id)
        ser = UserSerializer(user)
        return Response(ser.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authenticated
def update_profile(req, *args, **kwargs):
    try:
        user = User.objects.get(id=req.user.id)
        ser = UpdateUserSerializer(user, data=req.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.validated_data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authenticated
@reauthenticate
def change_password(req, user: User, *args, **kwargs):
    try:
        p1 = req.data.get('new-password', None)
        p2 = req.data.get('confirm-new-password', None)
        if p1 is None or p2 is None: raise MissingInput('new password/s not provided')
        if p1 != p2: raise InvalidPassword('passwords do NOT match')
        if len(p1) < 6: raise InvalidPassword("password length MUST be 6 characters or more")
        user.set_password(p1)
        user.save(update_fields=['password'])
        return Response(status=status.HTTP_200_OK)
    except (MissingInput, InvalidPassword) as err:
        return Response({'message': err.args[0]}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authenticated
@reauthenticate
def change_username(req, user: User, *args, **kwargs):
    try:
        username = req.data.get('new-username', None)
        if username is None: raise MissingInput('new username was not provided')
        validate_username(username)
        if User.objects.filter(username=username).exists(): 
            raise ValidationError('username already exists')
        user.username = username
        user.save(update_fields=['username'])
        return Response(status=status.HTTP_200_OK)
    except (MissingInput, ValidationError) as err:
        return Response({'message': err.args[0]}, status=status.HTTP_400_BAD_REQUEST)



# Updating email
@api_view(['POST'])
@authenticated
def request_email_verification(req, *args, **kwargs):
    try:
        email = req.data.get("email", None)
        if email is None: 
            raise MissingInput("email not provided")
        validate_email(email)
        User.objects.filter(id=req.user.id).update(email=email, is_email_verified=False)
        send_verification_email(email, get_base_url(req))
        return Response(status=status.HTTP_202_ACCEPTED)
    except MissingInput as err:
        return Response({'message': err.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'message': "invalid email"})
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authenticated
def resend_email_verification(req, *args, **kwargs):
    try:
        user = User.objects.get(id=req.user.id)
        if user.email and not user.is_email_verified:
            send_verification_email(user.email, get_base_url(req))
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response({'message': "email not found or already verified"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def verify_email(request, token, *args, **kwargs):
    try:
        enc = TodoemEncryption(token=token)
        email = enc.decrypt()
        res = User.objects.filter(email=email, is_email_verified=False).update(is_email_verified=True)
        if res != 1: raise ObjectDoesNotExist()
        return render(request, 'email_verified.html', {'email': email})
    except ObjectDoesNotExist:
        return render(request, 'account_not_found.html')
    except Exception as e:
        return render(request, 'error.html')



@api_view(['POST'])
@authenticated
@reauthenticate
def deactivate_account(req, user: User, *args, **kwargs):
    try:
        i, _ = user.delete()
        if i != 1:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def forgot_password(req, *args, **kwargs):
    try:
        email = req.data.get("email", None)
        if email is None: 
            raise MissingInput("email not provided")
        validate_email(email)
        user = User.objects.get(email=email)
        
        send_reset_password_email(email, get_base_url(req), user)
        
        return Response(status=status.HTTP_202_ACCEPTED)
    except MissingInput as err:
        return Response({'message': err.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response({'message': "invalid email"})
    except User.DoesNotExist:
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def rest_forgot_password(request, raw_token, *args, **kwargs):
    try:
        enc = TodoemEncryption(token=raw_token)
        content = dict_email_data(enc.decrypt())
        if not content['action'] == 'reset-password':
            raise
    except:
        pass
