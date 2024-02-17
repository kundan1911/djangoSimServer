# consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class AlertConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("alerts_group", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data == 'PING':
            await self.send('PONG')

    async def disconnect(self, close_code):
        pass

    async def send_alert(self, event):
        # Send alerts to WebSocket clients
        self.send(text_data=event["message"])
