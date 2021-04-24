import json
from channels.generic.websocket import WebsocketConsumer

class TcConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
    def receive(self, text_data):
        data = json.loads(text_data)
        if data['status'] == 'newProject':
            self.send(text_data=json.dumps({
                'project': data
            }))
        

    def disconnect(self):
        pass