from django.urls import path
from . import views as v

urlpatterns = [
    path("create/", v.create_tasklist),
    
    # sent
    path('list-sent/', v.list_sent_tasklist)
]
