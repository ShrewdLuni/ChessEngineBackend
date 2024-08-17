from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns = [
  path('ws/chess/', MyConsumer.as_asgi()),
]
