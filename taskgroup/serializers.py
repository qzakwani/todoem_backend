from rest_framework import serializers

from lister.serializers import ListerSerializer

from .models import TaskGroup, TaskGroupTask, TaskGroupMember



class TaskGroupMemberSerializer(serializers.ModelSerializer):
    member = ListerSerializer()
    class Meta:
        model = TaskGroupMember
        fields = '__all__'


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        exclude = ['members']
        read_only_fields = ['id', 'creator', 'created_at']



class TaskGroupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroupTask
        fields = '__all__'
        read_only_fields = ['id', 'taskgroup', 'edited', 'created_by', 'completed' ,'completed_by', 'comment', 'last_modified', 'created_at']


