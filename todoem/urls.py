from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    path('task/', include('task.urls')),
    path('lister/', include('lister.urls')),
    path('tasklist/', include('tasklist.urls')),
    path('taskgroup/', include('taskgroup.urls')),
]
