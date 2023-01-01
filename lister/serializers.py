from rest_framework import serializers

from account.models import User

from .models import ConnectionRequest, ConnectedLister


class ListerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name']

class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = ListerSerializer()
    class Meta:
        model = ConnectionRequest
        fields = ['id', 'sender', 'sent_at']


class ConnectedListerSerializer(serializers.ModelSerializer):
    lister = ListerSerializer()
    class Meta:
        model = ConnectedLister
        fields = ['lister', 'date_connected']
