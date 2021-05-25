import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         self.fetch_message(text_data_json)

#     def fetch_message(self, data):
#         messages = Message.get_last_10_msg(self)
#         content = {
#             'message': self.load_msg_json(messages)
#         }
#         for m in content:
#             self.send_in_chat_message(m)

#     def send_in_chat_message(self, messages):
#         print(messages)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': messages
#             }
#         )

#     def chat_message(self, event):
#         message = event['message']
#         self.save_message(message)
#         self.send(text_data=json.dumps({
#             'message': message
#         }))

#     def save_message(self, message):
#         message = Message(content=message['message'])
#         message.save()

#     def load_msg_json(self, messages):
#         result = []
#         for msg in messages:
#             result.append(self.message_to_json(msg))
#         return result

#     def message_to_json(self, message):
#         return message.content

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        '''
            Etablish the connection
        '''
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)  # assure that data is in json
        self.commands[data['commands']](self, data)

    def sending_in_room_group(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        # print(f'event = {event}')
        message = event['message']
        async_to_sync(self.send(text_data=json.dumps(
            {'message': message}
        )))

    def fetch_message_db(self, data):
        message_db = Message.get_last_10_msg(self)
        content = self.messages_db_json(message_db)
        for msg in content:
            print(msg)
            self.sending_in_room_group(msg)

    def messages_db_json(self, messages):
        result = []
        for msg in messages:
            result.append(msg.content)
        return result

    def send_message(self, messages):
        # print('send_message :', message)
        message = messages['message']
        msg = Message(content=message)
        msg.save()
        self.sending_in_room_group(message)

    commands = {
        'send_message': send_message,
        'fetch_message_db': fetch_message_db

    }
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
