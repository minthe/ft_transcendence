import json

from channels.db import database_sync_to_async
from backend_app.models import MyUser, Chat, Message, Game
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class _Message:
# ---------- HANDLE FUNCTIONS ---------------------------------------
    async def handle_send_online_stats(self):
        online_stats = [
            {
                'user_id': instance['user_id'],
                'stat': instance['is_online']
            }
            for instance in self.connections
        ]
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.online.stats',
                'data': {
                    'online_stats': online_stats
                },
            }
        )

    async def handle_send_online_stats_on_disconnect(self):
        online_stats = [
            {
                'user_id': instance['user_id'],
                'stat': instance['is_online']
            }
            for instance in self.connections
        ]
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.online.stats.on.disconnect',
                'data': {
                    'online_stats': online_stats
                },
            }
        )

    async def handle_save_message_in_db(self, text_data_json):
        chat_id = self.get_and_check_id(text_data_json["data"]["chat_id"])
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if chat_id == -1 or user_id == -1: return
        message = text_data_json["data"]["message"]

        # Use await to call the async method in the synchronous context
        response_message = await self.create_message(user_id, chat_id, message)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.message.save.success',
                'data': {
                    'message': response_message,
                    'chat_id': chat_id
                },
            }
        )

    async def handle_send_chat_messages(self, text_data_json):
        chat_id = self.get_and_check_id(text_data_json["data"]["chat_id"])
        if chat_id == -1: return
        message_data = await self.get_chat_messages(chat_id)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.chat.messages',
                'data': {
                    'chat_id': chat_id,
                    'message_data': message_data,
                },
            }
        )

    async def handle_messages_in_chat_read(self, text_data_json):
        chat_id = self.get_and_check_id(text_data_json["data"]["chat_id"])
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if chat_id == -1 or user_id == -1: return
        response = await self.set_messages_in_chat_read(user_id, chat_id)
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.message.in.chat.read',
                'data': {
                    'message': response,
                    'user_id': user_id
                },
            }
        )

    async def handle_messages_in_chat_unread(self, text_data_json):
        chat_id = self.get_and_check_id(text_data_json["data"]["chat_id"])
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if chat_id == -1 or user_id == -1: return
        response = await self.set_messages_in_chat_unread(user_id, chat_id)
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.message.in.chat.read',
                'data': {
                    'message': response,
                    'user_id': user_id
                },
            }
        )

# ---------- SEND FUNCTIONS ---------------------------------------
    async def send_chat_messages(self, event):
        await self.send(text_data=json.dumps({
            'type': 'all_chat_messages',
            'chat_id': event['data']['chat_id'],
            'message_data': event['data']['message_data'],
        }))

    async def send_message_save_success(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message_save_success',
            'message': event['data']['message'],
        }))

    async def send_online_stats(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_stats',
            'online_stats': event['data']['online_stats']
        }))

    async def send_online_stats_on_disconnect(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_stats_on_disconnect',
            'online_stats': event['data']['online_stats']
        }))

    async def send_message_in_chat_read(self, event):
        await self.send(text_data=json.dumps({
            'type': 'set_message_stat',
            'message': event['data']['message'],
            'user_id': event['data']['user_id']
        }))
# ---------- DATABASE REQUEST FUNCTIONS -----------------------------

    @database_sync_to_async
    def create_message(self, user_id, chat_id, text):
        try:
            if not text:
                return 'Message is empty'
            user_instance = MyUser.objects.get(user_id=user_id)
            specific_timestamp = timezone.now()
            new_message = Message.objects.create(senderId=user_id, sender=user_instance.name, text=text,
                                                 timestamp=specific_timestamp)
            chat_instance = Chat.objects.get(id=chat_id)
            chat_instance.messages.add(new_message.id)
            new_message.save()

            chat_instance = user_instance.objects.get(id=chat_id)
            chat_instance.is_read = False

            return 'ok'
        except Exception as e:
            return f'something big in createMessage: {e}'

    @database_sync_to_async
    def create_message_chatbot(self, invited_user_name, message):
        try:
            chat_name = 'CHAT_BOT'
            user_instance = MyUser.objects.get(name=invited_user_name)
            chat_instance = user_instance.chats.get(chatName=chat_name)
            specific_timestamp = timezone.now()
            new_message = Message.objects.create(senderId=chat_instance.id, sender=chat_name, text=message,
                                                 timestamp=specific_timestamp)
            chat_instance.messages.add(new_message.id)
            chat_instance.is_read = False
            new_message.save()
            chat_instance.save()
            return 'ok'
        except Exception as e:
            return f'something big in create_message_chatbot: {e}'

    @database_sync_to_async
    def get_chat_messages(self, chat_id):
        chat_instance = Chat.objects.get(id=chat_id)
        messages_in_chat = chat_instance.messages.all()
        message_data = [
            {
                'id': message.id,
                'sender_id': message.senderId,
                'sender': message.sender,
                'text': message.text,
                'timestamp': message.formatted_timestamp(),
            }
            for message in messages_in_chat
        ]
        return message_data


    @database_sync_to_async
    def set_messages_in_chat_read(self, user_id, chat_id):
        try:
            user_instance = MyUser.objects.get(user_id=user_id)
            chat_instance = user_instance.chats.get(id=chat_id)
            chat_instance.is_read = True
            chat_instance.save()
            return 'ok'
        except Exception as e:
            print(f'something big in set_messages_in_chat_read: {e}')
            return f'something big in set_messages_in_chat_read: {e}'


    @database_sync_to_async
    def set_messages_in_chat_unread(self, user_id, chat_id):
        try:
            user_instance = MyUser.objects.get(user_id=user_id)
            chat_instance = user_instance.chats.get(id=chat_id)
            chat_instance.is_read = False
            chat_instance.save()
            return 'ok'
        except Exception as e:
            print(f'something big in set_messages_in_chat_unread: {e}')
            return f'something big in set_messages_in_chat_unread: {e}'
# ---------- UTILS FUNCTIONS ----------------------------------------