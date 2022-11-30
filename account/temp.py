from django.utils.functional import cached_property

class TempUser:
        
    def __init__(self, token):
        self.token = token
    
    def __str__(self):
        return f"uid {self.id}"
    
    @cached_property
    def id(self):
        return self.token['uid']
    
    @cached_property
    def is_authenticated(self):
        return True
    