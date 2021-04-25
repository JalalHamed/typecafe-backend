import json
from channels.generic.websocket import AsyncWebsocketConsumer # change it from sync to async


class TcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'tc',
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self):
        await self.channel_layer.group_discard(
            'tc',
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data['status']
        if status == 'newProject':
            await self.send(text_data=json.dumps({
                'data': data
            }))
        if status == 'time':
            await self.channel_layer.group_send('tc', {
                'type': 'time',
                'data': json.dumps(data)
            })
        
    async def time(self, event):
        await self.send(text_data=json.dumps({
            'data': event
        }))

    