from django.db import models

from account.models import User


class Task(models.Model):
    FREQUENCY = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    ]
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    due = models.DateTimeField(blank=True)
    repeat = models.BooleanField(default=False)
    repeat_frequency = models.CharField(max_length=1, choices=FREQUENCY, default='D')
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)