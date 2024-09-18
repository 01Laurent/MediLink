import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user'].username

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
#         sender = self.scope['user']

#         # Save message to the database
#         await self.save_message(sender, message)

#         # Send message to the room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': sender.username,
#                 'profile_image': sender.profile_image_url,
#             }
#         )

#     async def chat_message(self, event):
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'profile_image': event['profile_image'],
#         }))

#     @sync_to_async
#     def save_message(self, sender, message):
#         recipient = self.get_recipient_from_room(self.room_name)
#         Message.objects.create(sender=sender, recipient=recipient, content=message)

#     @sync_to_async
#     def get_recipient_from_room(self, room_name):
#         # Split the room name to get the recipient username
#         usernames = room_name.split('_')
#         recipient_username = [u for u in usernames if u != self.scope['user'].username][0]
#         return User.objects.get(username=recipient_username)