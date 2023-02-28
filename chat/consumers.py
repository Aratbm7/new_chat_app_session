from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import GroupChat, Message, CustomSession
import json


# class EchoCunsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, code):
#         pass

#     async def receive(self, text_data):
#         self.send(text_data=text_data)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.domain_name = self.scope['headers'][0][1].decode('UTF-8').split(':')[0]
        # print('domain_name :', self.domain_name)
        self.session_key = self.scope['session'].session_key
        print('self.session_key=', self.session_key)
        sync_to_async(self.scope['session'].save)()
        self.chat = await self.get_chat()
        self.room_name = self.chat.unique_code
        print('room_name =', self.room_name)
        # print("scope ==", self.scope)
        self.room_group_name = "chat_%s" % self.room_name 
        print('room_group_name = ', self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # pip Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("text_data_json ==", text_data_json)
        message = text_data_json["message"]
        username = text_data_json['username']
        
        await self.create_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, 'username': username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event['username']
        print("event==", event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, 'username': username}))

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = GroupChat.objects.get(creator=self.session_key)
            return chat
        except GroupChat.DoesNotExist:
            return None


    @database_sync_to_async
    def create_message(self, text):
        customs_session = CustomSession.objects.get(session_key=self.session_key)
        Message.objects.create(chat_id=self.chat.id, anon_author=customs_session, text=text)