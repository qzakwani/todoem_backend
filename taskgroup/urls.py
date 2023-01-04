from django.urls import path


from . import views as v


urlpatterns = [
    path('create/', v.create_taskgroup),
    path('<int:taskgroup_id>/update/', v.update_taskgroup),
    
    path('<int:taskgroup_id>/', v.get_taskgroup),
    path('my/', v.list_my_taskgroup),
    path('all/', v.list_all_taskgroup),
    
    path('<int:taskgroup_id>/member/<int:lister_id>/', v.get_member),
    path('<int:taskgroup_id>/member/', v.get_all_members),
    
    
    path('<int:taskgroup_id>/task/<int:task_id>/', v.get_task),
    path('<int:taskgroup_id>/task/', v.get_all_tasks),
    
    # path('t/', v.testo)
]