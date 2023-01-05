from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.docs),
    path("schema/", v.schema, name='schema'),
]
