from django.urls import path
from .views import room, index, MessageView, home

urlpatterns = [
    path('', home, name='home'),
    path('chat/', index, name='index'),
    path('chat/<str:room_name>/', room, name='room'),
    path('api/msg/', MessageView.as_view(), name='api-msg')
]
