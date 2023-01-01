from django.urls import path


from . import views as v


urlpatterns = [
    # path('create/', v.create_taskgroup),
    # path('update/<int:taskgroup_id>/', v.update_taskgroup),
    # path('delete/<int:taskgroup_id>/', v.delete_taskgroup),
    
    # path('', v.my_taskgroup),
    # path('all/', v.list_taskgroup),
    
    
    # # Admin Action
    # path('add-member/<int:taskgroup_id>/<int:member_id>/', v.add_member),
    # path('kick-member/<int:taskgroup_id>/<int:member_id>/', v.kick_member),
    
    path('t/', v.testo)
]