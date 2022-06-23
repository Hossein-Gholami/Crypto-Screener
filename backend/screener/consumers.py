import json
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from . import tasks

class ChatConsumer(AsyncWebsocketConsumer):
    group_name = settings.STREAM_SOCKET_GROUP_NAME

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        tasks.fetch_last_prices.apply_async()

        await self.accept()

        # await self.channel_layer.group_send(
        #     self.group_name,
        #     {
        #         'type': 'tester_message',
        #         'data': 'hello world!',
        #     }
        # )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # async def chat_message(self, event):
    #     message = event['message']
    #     name = event['name']

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'name': name
    #     }))

    async def send_prices(self, event):
        await self.send(text_data=json.dumps({
            'tickers': event['tickers']
        }))

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     name = text_data_json['name']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message,
    #             'name': name
    #         }
    #     )

