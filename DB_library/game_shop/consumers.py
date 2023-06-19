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
        

class MyConsumer(WebsocketConsumer):

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
        self.user_name = user_name
        self.group_name = f"room_{room}"
        
        # accept connection
        self.accept() 
        
        # this will be sent only to the current user
        self.send(text_data=json.dumps({'message': "Welcome to chat room.  \
                                        please keep rules and respect bla bla.."}))
                        
        async_to_sync(self.channel_layer.group_add)(
                self.group_name, 
                self.channel_name)    

        # let everyone know that a new user entered
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                'type': 'global_handler',  # this is a function
                'message': f"user {user_name} entered!",
                'event_type': 'info' # optional extra info
                }
            )                    
    

    def receive(self, text_data):
        
        text_data = json.loads(text_data)
        msg = f"{self.user_name} :" + text_data['message']        

        # send back to sender (only):
        # self.send(text_data=json.dumps({'message': f'message received: {msg}'}))

        # forward msg to whole group:
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
                    'type': 'global_handler',  # this is a function
                    'message': msg,
                    'event_type': 'routine' # optional extra info
                }
            )


    def global_handler(self, event):
        """ This function will be run by each channel """

        self.send(text_data=json.dumps(
            {'message': event['message'],
             'event_type': event['event_type']}))
        

    def disconnect(self, code):
        """ This will be run when a user disconnected """

        msg = f"user {self.user_name} disconnected"
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {
            'type': 'global_handler',  # this is a function
            'message': msg,
            'event_type': 'info'}
            )