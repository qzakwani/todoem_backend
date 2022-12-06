from django.urls import path
from . import views as v

urlpatterns = [
    path('connection-request/', v.get_connection_request),
    path('connection-request/<int:user_id>/', v.send_connection_request),
    path('connection-accept/<int:user_id>/', v.accept_connection_request),
    path('connection-reject/<int:user_id>/', v.reject_connection_request),
    
    path('connection-status/<int:lister_id>/', v.connection_status),
    
    path('my-listers/', v.list_my_listers),
    path('search/', v.search_listers)
]