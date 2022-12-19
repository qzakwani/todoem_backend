from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/taskgroup/<str:group_id>/", consumers.ChatConsumer.as_asgi()),
]