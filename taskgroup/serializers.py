from rest_framework import serializers

from lister.serializers import ListerSerializer

from .models import TaskGroup, TaskGroupTask, TaskGroupMember


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = '__all__'
        read_only_fields = ['id', 'admin','listers', 'last_modified', 'created_at']



class TaskGroupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroupTask
        fields = '__all__'
        read_only_fields = ['id', 'taskgroup', 'edited', 'created_by', 'completed' ,'completed_by', 'comment', 'last_modified', 'created_at']



class TaskGroupMemberSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField('_member')
    
    def _member(self, obj):
        return ListerSerializer(self.context['member']).data
    
    class Meta:
        model = TaskGroupMember
        fields = '__all__'
