from rest_framework import serializers


from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        
        fields = [
            'id',
            'user_id',
            'task',
            'completed',
            'due',
            'repeat',
            'repeat_frequency',
            'description',
            'created_at'
        ]
        
        read_only_fields = ['id', 'user_id','created_at']
