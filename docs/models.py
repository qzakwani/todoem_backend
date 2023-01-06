from django.db import models

# Create your models here.
class Path(models.Model):
    METHODS = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("DELETE", "DELETE"),
        ("UPDATE", "UPDATE"),
    )
    
    path = models.CharField(max_length=300)
    method = models.CharField(max_length=10, choices=METHODS, default="GET")


class PathItem(models.Model):
    path = models.ForeignKey("docs.Path", on_delete=models.CASCADE)
    TAGS = (
        ("Account", "Account"),
        ("Lister", "Lister"),
        ("Task", "Task"),
        ("TaskList", "TaskList"),
        ("TaskGroup", "TaskGroup"),
    )
    tags = models.CharField(max_length=50, choices=TAGS)
    summary = models.CharField(max_length=250)
    description = models.TextField(blank=True)



class RequestBody(models.Model):
    path_item = models.ForeignKey("docs.PathItem", on_delete=models.CASCADE)
    
    CONTENT_TYPE = (
        ("application/json", "application/json"),
        ("multipart/form-data", "multipart/form-data"),
    )
    
    content = models.CharField(max_length=50, choices=CONTENT_TYPE, default="application/json")
    
    schema = models.JSONField()

class PathSchema(models.Model):
    METHODS = (
        ("GET", "GET"),
        ("POST", "POST"),
        ("DELETE", "DELETE"),
        ("UPDATE", "UPDATE"),
    )
    
    path = models.CharField(max_length=300)
    method = models.CharField(max_length=10, choices=METHODS, default="GET")
    schema = models.TextField()