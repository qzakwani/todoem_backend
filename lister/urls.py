from django.urls import path
from . import views as v

urlpatterns = [
    path('connection-request/<int:user_id>/', v.send_connection_request)
]