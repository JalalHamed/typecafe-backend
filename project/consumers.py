from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
from time import sleep


class ProjectConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(1000):
            self.send(json.dump({'message': randint(1, 100)}))
            sleep(1)