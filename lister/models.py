from django.db import models
from django.conf import settings


class Lister(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='me')
    lister = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    date_connected = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'lister'], name='unique_request', violation_error_message='lister connected already')
        ]
    
    def __str__(self) -> str:
        return f'{self.user.username} to {self.lister.username}'




class ConnectionRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_request', violation_error_message='request has already been sent')
        ]

    
    def __str__(self) -> str:
        return f'{self.sender.username} to {self.receiver.username}'