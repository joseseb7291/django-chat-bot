import json
from chatbot_tutorial.models import JokeCount
from channels.generic.websocket import AsyncWebsocketConsumer
from chatbot_tutorial.views import respond_to_websockets
from asgiref.sync import sync_to_async

from channels.db import database_sync_to_async



class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    @database_sync_to_async
    def save_entry_to_db(self, joke_type, user):
        joke = JokeCount(joke_word=joke_type, user=user)
        joke.save()
        return True

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        joke_type = text_data_json['type']
        user = text_data_json['user']
        response = respond_to_websockets(joke_type)
        await self.save_entry_to_db(joke_type, user)
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': response,
            }
        )

    async def chat_message(self, event):
        message = event['text']

        await self.send(text_data=json.dumps({
            'message': message,
        }))
