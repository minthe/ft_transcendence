import json

from channels.db import database_sync_to_async
from backend_app.models import MyUser, Chat, Message, Game
from django.core.exceptions import ObjectDoesNotExist


class _User:

# ---------- HANDLE FUNCTIONS ---------------------------------------
    async def handle_send_user_in_current_chat(self, chat_id):
        user_in_chat = await self.get_user_in_chat(chat_id)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.user.in.current.chat',
                'data': {
                    'chat_id': chat_id,
                    'user_in_chat': user_in_chat,
                },
            }
        )

    async def handle_send_all_user(self):
        all_user = await self.get_all_user()
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.all.user',
                'data': {
                    'all_user': all_user
                },
            }
        )

    async def handle_current_user_left_chat(self, text_data_json):
        chat_id = text_data_json["data"]["chat_id"]
        user_id = text_data_json["data"]["user_id"]
        info = await self.leaveChat(user_id, chat_id)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.user.left.chat',
                'data': {
                    'message': info
                },
            }
        )

    async def handle_get_avatar(self, text_data_json):
        user_id = text_data_json["data"]["user_id"]
        response = await self.get_avatar(user_id)

        await self.send(text_data=json.dumps({
            'type': 'get_avatar',
            'avatar': response,
        }))


# ---------- SEND FUNCTIONS ---------------------------------------
    # TODO: MARIE: ever used? delete?
    async def send_user(self, user_id, message):
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            **message,
        }))
    async def send_user_in_current_chat(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_in_current_chat',
            'user_in_chat': event['data']['user_in_chat']
        }))

    async def send_all_user(self, event):
        await self.send(text_data=json.dumps({
            'type': 'all_user',
            'all_user': event['data']['all_user']
        }))


# ---------- DATABASE REQUEST FUNCTIONS -----------------------------

    @database_sync_to_async
    def get_user_in_chat(request, chat_id):
        chat_instance = Chat.objects.get(id=chat_id)
        all_user_in_current_chat = MyUser.objects.filter(chats=chat_instance)
        user_in_chat = [
            {
                'user_name': user.name,
                'user_id': user.id
            }
            for user in all_user_in_current_chat
        ]
        return user_in_chat

    @database_sync_to_async
    def leaveChat(self, user_id, chat_id):
        try:
            user_exists = MyUser.objects.filter(id=user_id).exists()
            if not user_exists:
                return 'User in leaveChat not found'
            chat_exists = Chat.objects.filter(id=chat_id).exists()
            if not chat_exists:
                return 'Chat in leaveChat not found'
            chat_instance = Chat.objects.get(id=chat_id)
            user_instance = MyUser.objects.get(id=user_id)
            user_instance.chats.remove(chat_instance)
            user_instance.save()
            return 'ok'
        except Exception as e:
            return 'something big in leaveChat'

    @database_sync_to_async
    def get_all_user(self):
        all_users_info = MyUser.objects.values('id', 'name')
        all_user = list(all_users_info)
        return all_user

    @database_sync_to_async
    def get_avatar(self, user_id):
        user_exists = MyUser.objects.filter(id=user_id).exists()
        if not user_exists:
            return None
        user_instance = MyUser.objects.get(id=user_id)
        avatar_url = user_instance.avatar.url if user_instance.avatar else None
        result = '../../backend' + str(avatar_url) if avatar_url else None
        return result

# ---------- UTILS FUNCTIONS ----------------------------------------