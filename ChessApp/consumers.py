import json
import random
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        random_int = random.randint(1, 100)
        
        self.send(text_data=json.dumps({
            'random_int': random_int
        }))
