from rest_framework import serializers

from .models import TaskList, TaskListTask

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

class TaskListSerializer(serializers.ModelSerializer):
    tasks = TaskListTaskSerializer(many=True)
    class Meta:
        model = TaskList
        fields = [
            'id',
            'name',
            'description',
            'completed',
            'sender_id',
            'receiver_id',
            'tasks',
            'notification',
            'created_at'
        ]
        
        read_only_fields = ['id', 'sender_id','receiver_id', 'notification', 'created_at']
        
        
        
