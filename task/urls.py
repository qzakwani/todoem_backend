from django.urls import path

from . import views as v

urlpatterns = [
    path('create/', v.create_task),
    path('<int:task_id>/', v.get_task),
    path('list/', v.list_tasks),
    path('update/<int:task_id>/', v.update_task),
    path('complete/<int:task_id>/', v.complete_task),
    path('uncomplete/<int:task_id>/', v.uncomplete_task),
    path('delete/<int:task_id>/', v.delete_task),
    path('delete-all-completed/', v.delete_completed_tasks),
    path('delete-all/', v.delete_tasks),
]
