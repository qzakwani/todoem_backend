from django.db import models
from django.conf import settings
from django.utils import timezone



class TaskGroup(models.Model):
    name = models.CharField(max_length=150)
    purpose = models.CharField(max_length=250)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taskgroup_admin')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='member') 
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.admin.id}: {self.name}'




class TaskGroupTask(models.Model):
    taskgroup = models.ForeignKey('taskgroup.TaskGroup', on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    due = models.DateTimeField(blank=True, null=True)
    
    last_modified = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    