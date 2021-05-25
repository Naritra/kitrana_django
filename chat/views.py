from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import Response
from .models import Chat, Message
from rest_framework.views import APIView
from .serializers import MessageSerializer
# Create your views here.


def home(request):
    return render(request, 'chat/home.html')


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html',
                  {'room_name': room_name})


class MessageView(APIView):
    def get(self, request, *args, **kwargs):
        query = Message.objects.all()
        serializer = MessageSerializer(instance=query, many=True)
        return Response(serializer.data)
