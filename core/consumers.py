import json
from django.db.models import F
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from account.models import *
from project.models import *
from message.models import *


class TcConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'tc',
            self.channel_name
        )
        await self.accept()
        await self.update_user_inc(self.scope['user'])
        await self.channel_layer.group_send('tc', {
            'type': 'user_online',
            'user_id': self.scope['user'].id,
        })

    async def disconnect(self, close_code):
        await self.update_user_dec(self.scope['user'])
        online_count = await self.get_user_online_count(self.scope['user'].id)
        if online_count == 0:
            await self.update_user_last_login(self.scope['user'])
            await self.channel_layer.group_send('tc', {
                'type': 'user_offline',
                'user_id': self.scope['user'].id,
            })
        await self.channel_layer.group_discard(
            'tc',
            self.channel_name
        )

    async def receive(self, text_data=None):
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
        if data['status'] == 'offer-delete':
            await self.channel_layer.group_send('tc', {
                'type': 'offer_delete',
                'data': data,
            })
        if data['status'] == 'new-message':
            await self.channel_layer.group_send('tc', {
                'type': 'new_message',
                'data': data,
            })
        if data['status'] == 'offer-rejected':
            await self.channel_layer.group_send('tc', {
                'type': 'offer_rejected',
                'data': data,
            })
        if data['status'] == 'client-accept':
            await self.channel_layer.group_send('tc', {
                'type': 'client_accept',
                'data': data,
            })
        if data['status'] == 'in-progress':
            await self.channel_layer.group_send('tc', {
                'type': 'in_progress',
                'data': data,
            })

    async def user_online(self, event):
        await self.send(text_data=json.dumps({
            'ws_type': 'user-online',
            'user_id': event['user_id'],
        }))

    async def user_offline(self, event):
        await self.send(text_data=json.dumps({
            'ws_type': 'user-offline',
            'user_id': event['user_id'],
        }))

    async def new_project(self, event):
        project = await self.get_project(event['data']['id'])
        client = await self.get_user_with_email(event['data']['user_email'])
        client_image = ""
        if client['image']:
            client_image = '/media/' + client['image']
        await self.send(text_data=json.dumps({
            'ws_type': 'new-project',
            'id': project['id'],
            'description': project['description'],
            'file': 'http://127.0.0.1:8000/media/' + project['file'],
            'languages_and_additions': project['languages_and_additions'],
            'number_of_pages': project['number_of_pages'],
            'delivery_deadline': project['delivery_deadline'],
            'description': project['description'],
            'type': project['type'],
            'created_at': str(project['created_at']),
            'status': project['status'],
            'client': client['displayname'],
            'client_id': client['id'],
            'client_email': client['email'],
            'client_image': client_image,
            'client_is_online': client['is_online'],
            'client_last_login': str(client['last_login']),
        }))

    async def delete_project(self, event):
        await self.send(text_data=json.dumps({
            'ws_type': 'delete-project',
            'id': event['data']['id'],
        }))

    async def new_offer(self, event):
        user = self.scope['user'].__dict__['token']['user_id']
        offer = await self.get_offer(event['data']['id'])
        typist = await self.get_user_with_email(event['data']['user_email'])
        project = await self.get_project(event['data']['project_id'])
        typist_image = ""
        if typist['image']:
            typist_image = '/media/' + typist['image']
        if user == project['client_id']:
            await self.send(text_data=json.dumps({
                'ws_type': 'new-offer',
                'id': offer['id'],
                'project': offer['project_id'],
                'typist': typist['displayname'],
                'typist_image': typist_image,
                'typist_id': typist['id'],
                'offered_price': offer['offered_price'],
                'created_at': str(offer['created_at']),
                'status': offer['status'],
            }))

    async def offer_delete(self, event):
        user = self.scope['user'].__dict__['token']['user_id']
        if user == event['data']['project_owner']:
            await self.send(text_data=json.dumps({
                'ws_type': 'delete-offer',
                'id': event['data']['id'],
            }))

    async def new_message(self, event):
        user = self.scope['user'].__dict__['token']['user_id']
        sender = await self.get_user_with_id(event['data']['sender_id'])
        message = await self.get_message(event['data']['id'])
        sender_image = ""
        if sender['image']:
            sender_image = '/media/' + sender['image']
        if user == event['data']['receiver']:
            await self.send(text_data=json.dumps({
                'ws_type': 'new-message',
                'id': message['id'],
                'sor': 'received',
                'content': message['content'],
                'is_read': message['is_read'],
                'issue_date': str(message['issue_date']),
                'sender_id': sender['id'],
                'sender_displayname': sender['displayname'],
                'sender_image': sender_image,
                'sender_is_online': sender['is_online'],
                'sender_last_login': str(sender['last_login']),
            }))

    async def offer_rejected(self, event):
        user = self.scope['user'].__dict__['token']['user_id']
        offer = await self.get_offer(event['data']['id'])
        if user == offer['typist_id']:
            await self.send(text_data=json.dumps({
                'ws_type': 'offer-rejected',
                'project': offer['project_id'],
                'id': offer['id'],
            }))

    async def client_accept(self, event):
        user = self.scope['user'].__dict__['token']['user_id']
        offer = await self.get_offer(event['data']['id'])
        if user == offer['typist_id']:
            await self.send(text_data=json.dumps({
                'ws_type': 'client-accept',
                'project': offer['project_id'],
                'client': event['data']['client'],
                'issued_at': event['data']['issued_at'],
                'offer': offer['id'],
            }))

    async def in_progress(self, event):
        project = await self.get_project(event['data']['project'])
        await self.send(text_data=json.dumps({
            'ws_type': 'in-progress',
            'project': project['id'],
        }))

    @ database_sync_to_async
    def get_project(self, project_id):
        return Project.objects.get(id=project_id).__dict__

    @ database_sync_to_async
    def get_user_with_id(self, user_id):
        return Account.objects.get(id=user_id).__dict__

    @ database_sync_to_async
    def get_user_with_email(self, user_email):
        return Account.objects.get(email=user_email).__dict__

    @ database_sync_to_async
    def get_offer(self, offer_id):
        return Offer.objects.get(id=offer_id).__dict__

    @ database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.get(id=message_id).__dict__

    @ database_sync_to_async
    def get_user_online_count(self, user_id):
        return Account.objects.get(id=user_id).is_online

    @ database_sync_to_async
    def update_user_inc(self, user):
        return Account.objects.filter(id=user.id).update(is_online=F('is_online') + 1)

    @ database_sync_to_async
    def update_user_dec(self, user):
        return Account.objects.filter(id=user.id).update(is_online=F('is_online') - 1)

    @ database_sync_to_async
    def update_user_last_login(self, user):
        return Account.objects.filter(id=user.id).update(last_login=timezone.now())
