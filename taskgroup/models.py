from django.db import models
from django.conf import settings
# from django.utils import timezone



class TaskGroup(models.Model):
    name = models.CharField(max_length=150)
    purpose = models.CharField(max_length=250)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taskgroup_creator')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TaskGroupMember') 
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'id: {self.id} -> creator: {self.creator.id}'




class TaskGroupMember(models.Model):
    taskgroup = models.ForeignKey('TaskGroup', on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['taskgroup', 'member'], name='unique_member', violation_error_message='lister already added')
        ]



class TaskGroupTask(models.Model):
    taskgroup = models.ForeignKey('TaskGroup', on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by')
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    due = models.DateTimeField(blank=True, null=True)
    
    last_modified = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
