import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class TcConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'tc',
            self.channel_name
        )
        self.accept()
        
    def receive(self, text_data):
        data = json.loads(text_data)
        status = data['status']
        if status == 'newProject':
            self.send(text_data=json.dumps({
                'data': data
            }))
        if status == 'time':
            async_to_sync(self.channel_layer.group_send)('tc', {
                'type': 'time',
                'data': json.dumps(data)
            })
        
    def time(self, event):
        self.send(text_data=json.dumps({
            'data': event
        }))

    def disconnect(self, close_code):
        print('disconnected', close_code)