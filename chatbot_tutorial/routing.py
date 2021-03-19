
from .wsgi import *  # add this line to top of your code
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chatbot_tutorial import consumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('chat/stream/<str:room_name>/', consumer.ChatRoomConsumer.as_asgi()),
        ])
    ),
})
