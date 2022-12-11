from django.db import models
from django.conf import settings


class TaskList(models.Model):
    name = models.CharField(max_length=50, default="Task List")
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False) 
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasklist_sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasklist_receiver")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name


class TaskListTask(models.Model):
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.tasklist.id} : {self.task}'
    