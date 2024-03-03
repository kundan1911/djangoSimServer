# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class AlertConsumer(WebsocketConsumer):
    def connect(self):
        # self.channel_layer.group_add("alerts_group", self.channel_name)
        self.room_group_name = "alerts_group"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        self.send(text_data=json.dumps({ 'type':"connection estasbled",'message':'hi from server'   }))

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data == 'PING':
            await self.send('PONG')

    async def disconnect(self, close_code):
        pass

    def send_alert(self, event):
        # Send alerts to WebSocket clients
        print("calling send_allertttttt")
        self.send(text_data=event["message"])

