from rest_framework import serializers

from .models import TaskList, TaskListTask

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = [
            'id',
            'name',
            'description',
            'completed',
            'sender_id',
            'receiver_id',
            'created_at'
        ]
        
        read_only_fields = ['id', 'sender_id','receiver_id','created_at']
        


class TaskListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskListTask
        fields = [
            'id',
            'tasklist',
            'task',
            'completed',
        ]
        
        read_only_fields = ['id', 'tasklist']