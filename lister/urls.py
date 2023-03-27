from django.urls import path
from . import views as v

urlpatterns = [
    path('id/<int:lister_id>/', v.get_lister),
    path('username/<str:username>/', v.get_lister_by_username),
    
    path('connection-requests/', v.get_connection_request),
    path('connection-request/<int:user_id>/', v.send_connection_request),
    path('connection-accept/<int:user_id>/', v.accept_connection_request),
    path('connection-reject/<int:user_id>/', v.reject_connection_request),
    path('connection-cancel/<int:lister_id>/', v.cancel_connection_request),
    
    path('connection-status/<int:lister_id>/', v.connection_status),
    
    path('my-listers/', v.list_my_listers),
    path('my-listers/search/', v.search_my_listers),
    path('disconnect/<int:lister_id>/', v.disconnect_lister),
    path('search/', v.search_listers)
]