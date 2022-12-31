from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/taskgroup/<int:taskgroup_id>/", consumers.TaskGroupConsumer.as_asgi()),
]