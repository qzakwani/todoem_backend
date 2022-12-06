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
            'sender',
            'receiver',
            'created_at'
        ]
        


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskListTask
        fields = [
            'id',
            'tasklist',
            'task',
            'completed',
        ]