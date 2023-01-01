from django.urls import path
from . import views as v

urlpatterns = [
    path("create/<int:to>/", v.send_tasklist),
    
    # sent
    path('list-sent/', v.list_sent_tasklist),
    path('get-sent-tasks/<int:list_id>/', v.get_sent_tasklist_tasks),
    path('delete-sent/<int:list_id>/', v.delete_sent_tasklist),
    path('check-delivery/<int:list_id>/', v.check_delivery_status),
    
    
    # received
    path('list/', v.list_tasklist),
    path('get-tasks/<int:list_id>/', v.get_tasklist_tasks),
    path('delete/<int:list_id>/', v.delete_tasklist),
    path('complete/<int:list_id>/', v.complete_tasklist),
    path('complete/<int:list_id>/<int:task_id>/', v.complete_tasklist_task),
    path('uncomplete/<int:list_id>/', v.uncomplete_tasklist),
    path('uncomplete/<int:list_id>/<int:task_id>/', v.uncomplete_tasklist_task),
    
]
