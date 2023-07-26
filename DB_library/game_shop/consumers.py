import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import urllib.parse


class Consumer(WebsocketConsumer):
    def connect(self):
        # parse parameters to get chat-room and user-name
        q_params_str = self.scope['query_string'].decode()
        pairs = q_params_str.split("&")
        room = None
        user_name = None
        for p in pairs:
            k_v = p.split("=")
            if k_v[0] == 'room':
                room = k_v[1]
            if k_v[0] == 'user':
                user_name = k_v[1]

        room = room if room else "global"
        user_name = user_name if user_name else "anonymous"
        self.user_name = urllib.parse.unquote(user_name)  # Decode user_name here
        self.group_name = f"room_{room}"

        # Accept connection
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Let everyone know that a new user entered
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'global_handler',

                'message': f"{self.user_name} הצטרף לצאט",  # Use self.user_name here
                'event_type': 'info'
            }
        )

    def receive(self, text_data):
        text_data = json.loads(text_data)
        msg = f"{self.user_name} : {text_data['message']}"  # Use self.user_name here

        # Forward msg to the whole group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'global_handler',
                'message': msg,
                'event_type': 'routine'
            }
        )

    def global_handler(self, event):
        """This function will be run by each channel"""

        self.send(text_data=json.dumps(
            {'message': event['message'],
             'event_type': event['event_type'],
            }
        ))

    def disconnect(self, code):
        """This will be run when a user disconnects"""

        msg = f"{self.user_name} התנתק מהצאט",   # Use self.user_name here
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'global_handler',
                'message': msg,
                'event_type': 'info'
            }
        )
