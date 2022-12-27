import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoem.settings')

django_asgi_app = get_asgi_application()

import taskgroup.routing

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AllowedHostsOriginValidator(
#             URLRouter(taskgroup.routing.websocket_urlpatterns)
#         ),
# })

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": 
            URLRouter(taskgroup.routing.websocket_urlpatterns)
        ,
})