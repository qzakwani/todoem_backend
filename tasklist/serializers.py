from rest_framework import serializers

from .models import TaskList

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = [
            'id',
            'name',
            'description',
            'completed',
            'sender',
            'receiver',
            'created_at'
        ]
        
        read_only_fields = ['id', 'created_at', 'completed', 'sender', 'reciever']
        