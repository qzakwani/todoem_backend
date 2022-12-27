from rest_framework import serializers


from .models import TaskGroup, TaskGroupTask


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = '__all__'
        read_only_fields = ['id', 'admin','listers', 'last_modified', 'created_at']



class TaskGroupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroupTask
        fields = '__all__'
        read_only_fields = ['id', 'taskgroup', 'completed' ,'completed_by', 'comment', 'last_modified', 'created_at']