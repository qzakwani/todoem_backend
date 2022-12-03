from django.db import models
from django.conf import settings


class Task(models.Model):
    FREQUENCY = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    ]
    
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    due = models.DateTimeField(blank=True, null=True)
    repeat = models.BooleanField(default=False)
    repeat_frequency = models.CharField(max_length=1, choices=FREQUENCY, default='D')
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f'{self.task}'