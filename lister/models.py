from django.db import models
from django.conf import settings
from account.models import User


class ConnectedListers(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    listers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="listers")
    
    
    def __str__(self) -> str:
        return self.user.username




class ConnectionRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    
    class Meta:
        unique_together = ['sender', 'receiver']
        

    
    def __str__(self) -> str:
        return f'{self.sender.username} to {self.receiver.username}'