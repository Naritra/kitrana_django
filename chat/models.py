from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_last_10_msg(self):
        '''
            Fetch last new 10 message
        '''
        return Message.objects.order_by('timestamp').all()[:10]

    def __str__(self) -> str:
        return self.content + '&' + str(self.id)


class Chat(models.Model):
    room_name = models.CharField(max_length=255)
    message = models.ManyToManyField(Message)

    def __str__(self) -> str:
        return self.room_name
