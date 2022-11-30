from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'password', 
            'first_name', 
            'last_name', 
            'email', 
            'phone_number',
            'date_joined'
            ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
    
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
