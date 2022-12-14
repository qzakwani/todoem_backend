from rest_framework import serializers

from .models import TaskList, TaskListTask, SentTaskList, SentTaskListTask
from .utils import insert_tasklist

################
#*    SENT    *#
################

class SentTaskListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentTaskListTask
        fields = [
            'id',
            'tasklist',
            'task',
        ]
        
        read_only_fields = ['id', 'tasklist']

class CreateSentTaskListSerializer(serializers.ModelSerializer):
    tasks = SentTaskListTaskSerializer(many=True)
    class Meta:
        model = SentTaskList
        fields = [
            'name',
            'description',
            'tasks',
        ]
        
        
    def create(self, validated_data):
        task_list = insert_tasklist(SentTaskList, SentTaskListTask, validated_data)
        return task_list


class ReadSentTaskListSerializer(serializers.ModelSerializer):
    tasks = SentTaskListTaskSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = SentTaskList
        fields = [
            'id',
            'name',
            'description',
            'sender_id',
            'receiver_id',
            'tasks',
            'tasks_num',
            'delivered',
        ]
        