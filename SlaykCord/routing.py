from django.urls import path
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import ChatConsumer

"""
Defines what connections are handled by consumers (URLRouter or ProtocolTypeRouter).
"""
application = ProtocolTypeRouter({
    # Route all WebSocket requests to chat handler and add users and sessions.
    # http://channels.readthedocs.io/en/latest/topics/routing.html
    # http://channels.readthedocs.io/en/latest/topics/authentication.html
    "websocket": AuthMiddlewareStack(URLRouter([path("chat/stream/", ChatConsumer)]))
})
