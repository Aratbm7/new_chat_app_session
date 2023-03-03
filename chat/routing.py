from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.AdminCunsumer.as_asgi()),
    re_path(r'ws/chat/', consumers.ChatConsumer.as_asgi()),
]