from django.db import models
from django.conf import settings
from django.db.models import Q



class ConnectedLister(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lister_user')
    lister = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lister_lister')
    
    date_connected = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'lister'], name='unique_connected_listers', violation_error_message='lister connected already')
        ]
    
    def __str__(self) -> str:
        return f'{self.user.username} to {self.lister.username}'




class ConnectionRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="request_receiver")
    
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_request', violation_error_message='request has already been sent'),
        ]

    
    def __str__(self) -> str:
        return f'{self.sender.username} to {self.receiver.username}'