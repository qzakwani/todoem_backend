from django.urls import path

from . import views as v

urlpatterns = [
    path('<int:task_id>/', v.get_task)
]
