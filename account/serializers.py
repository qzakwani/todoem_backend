from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login


from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'password', 
            'name', 
            'email', 
            'is_email_verified',
            'phone_number',
            'is_phone_number_verified',
            'date_joined'
            ]
        read_only_fields = ['id', 'date_joined', 'is_email_verified', 'is_phone_number_verified']
        extra_kwargs = {'password': {'write_only': True}}
    
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name', 
            ]



class LoginTokenSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data