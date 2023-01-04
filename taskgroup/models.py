from django.db import models
from django.conf import settings
# from django.utils import timezone
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class TaskGroup(models.Model):
    name = models.CharField(max_length=150)
    purpose = models.CharField(max_length=250)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), related_name='taskgroup_creator')
    
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
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET(get_sentinel_user))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), related_name='created_by')
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    due = models.DateTimeField(blank=True, null=True)
    edited = models.BooleanField(default=False)
    
    last_modified = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
