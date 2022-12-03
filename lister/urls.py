from django.urls import path
from . import views as v

urlpatterns = [
    path('connection-request/<int:user_id>/', v.send_connection_request),
    path('connection-accept/<int:user_id>/', v.accept_connection_request),
    path('connection-reject/<int:user_id>/', v.reject_connection_request),
]