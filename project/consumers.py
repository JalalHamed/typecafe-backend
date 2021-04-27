import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from account.models import Account
from .models import Project


class TcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'tc',
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'tc',
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data['status'] == 'new-project':
            await self.channel_layer.group_send('tc', {
                'type': 'new_project',
                'data': data,
            })
        if data['status'] == 'delete-project':
            await self.channel_layer.group_send('tc', {
                'type': 'delete_project',
                'data': data,
            })
        if data['status'] == 'new-offer':
            await self.channel_layer.group_send('tc', {
                'type': 'new_offer',
                'data': data,
            })

    async def new_project(self, event):
        project = await self.get_project(event['data']['id'])
        client = await self.get_client(event['data']['email'])
        client_image = ""
        if client['image']:
            client_image = '/media/' + client['image']
        await self.send(text_data=json.dumps({
            'ws_type': 'new-project',
            'id': project['id'],
            'description': project['description'],
            'file': '/media/' + project['file'],
            'languages_and_additions': project['languages_and_additions'],
            'number_of_pages': project['number_of_pages'],
            'delivery_deadline': project['delivery_deadline'],
            'description': project['description'],
            'type': project['type'],
            'created_at': str(project['created_at']),
            'status': project['status'],
            'client': client['displayname'],
            'client_email': client['email'],
            'client_image': client_image
        }))
    
    async def delete_project(self, event):
        await self.send(text_data=json.dumps({
            'ws_type': 'delete_project',
            'status': 'delete-project',
            'id': event['data']['id']
        }))

    @database_sync_to_async
    def get_project(self, project_id):
        return Project.objects.get(id=project_id).__dict__
    
    @database_sync_to_async
    def get_client(self, client_email):
        return Account.objects.get(email=client_email).__dict__