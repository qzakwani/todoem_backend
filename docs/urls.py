from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.docs),
    path("schema/", v.hello, name='schema'),
    path("urls/", v.list_urls, name='urls'),
    path("t/", v.hello, name='ccc'),
    
]
