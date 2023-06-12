from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class Consumer(WebsocketConsumer):

    def connect(self):

        params_str = self.scope['query_string'].decode()        
        print(params_str)

        self.accept()
        self.send(text_data=json.dumps({
            'message': "ws connected"
        }))
        self.groups_name = 'global'

        group_add_sync = async_to_sync(self.channel_layer.group_add)
        group_add_sync(self.groups_name, self.channel_name)

    def receive(self, text_data):
        msg = json.loads(text_data)
        print(msg)
        self.send(text_data=json.dumps({
            'message': 'Ack',
            'type': 'info',
        }))

        group_send_sync = async_to_sync(self.channel_layer.group_send)
        group_send_sync(self.groups_name, {
            'message': msg['message'],
            'type': 'group_send'
        })

    def group_send(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']}))

        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.groups_name,
                                                        self.channel_name)