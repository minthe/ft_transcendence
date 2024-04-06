import asyncio
import json
from django.http import JsonResponse
from backend_app.models import MyUser, Chat, Message, Game
from backend_app import utils
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.utils import timezone
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from backend_app.consumer.chat.user import _User
from backend_app.consumer.chat.messages import _Message
from backend_app.consumer.chat.chats import _Chat
from backend_app.consumer.game.game import _Game
from channels.generic.websocket import AsyncWebsocketConsumer

class WebsocketConsumer(AsyncWebsocketConsumer, _User, _Message, _Chat, _Game):
    connections = [
        {
            'user_id': '',
            'is_online': ''
        }
    ]

    channels = [
        {
            'user_id': '',
            'channel_name': ''
        }
    ]

    game_states = {}

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.channel_of_user = None
        self.my_group_id = None
        self.isOnline = 0
        self.key_code = 0
        self.prev_pos = 0
        self.is_host = 0
        self.game_id = 0
        self.game_group_id = None

    async def connect(self):
        user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user = {'user_id': user_id, 'is_online': 'true'}
        self.connections.append(self.user)
        await self.channel_layer.group_add('channel_zer0', self.channel_name)
        self.channel_of_user = {'user_id': user_id, 'channel_name': self.channel_name}
        self.channels.append(self.channel_of_user)
        await self.handle_send_online_stats()# ??
        await self.accept()

    async def disconnect(self, close_code):
        self.connections.remove(self.user)
        await self.handle_send_online_stats_on_disconnect()
        if self.game_group_id is not None:
            self.game_states[self.game_id]['game_active'] = False

            await self.channel_layer.group_send(
                self.game_group_id,
                {
                    'type': 'send.opponent.disconnected',
                    'data': {

                    },
                }
            )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        what_type = text_data_json["type"]

        # IF what_type is equal to a game request -> change later to something better
        if what_type in ['send_game_scene', 'send_init_game', 'send_ball_update', 'send_request_invites']:
            await self.controlGameRequests(text_data_json, what_type)
        else:
            chat_id = text_data_json["data"]["chat_id"]
            # user_id = text_data_json["data"]["user_id"]
            self.my_group_id = 'group_%s' % chat_id
            print('ADDED user ', self.user["user_id"], '  to group: ', self.my_group_id, ' || channel_name: ', self.channel_name, ' || type: ', text_data_json["type"])
            await self.channel_layer.group_add(self.my_group_id, self.channel_name)

            if what_type == 'save_message_in_db':
                await self.handle_save_message_in_db(text_data_json)
            elif what_type == 'send_chat_messages':
                await self.handle_send_chat_messages(text_data_json)
            elif what_type == 'send_online_stats':
                await self.handle_send_online_stats()
            elif what_type == 'send_user_in_current_chat':
                await self.handle_send_user_in_current_chat(chat_id)
            elif what_type == 'send_current_users_chats':
                await self.handle_send_current_users_chats(text_data_json)
            elif what_type == 'get_all_user':
                await self.handle_send_all_user()
            elif what_type == 'send_user_left_chat':
                await self.handle_current_user_left_chat(text_data_json)
            elif what_type == 'send_created_new_chat':
                await self.handle_create_new_public_chat(text_data_json)
            elif what_type == 'send_created_new_private_chat':
                await self.handle_create_new_private_chat(text_data_json)
            elif what_type == 'set_invited_user_to_chat':
                await self.handle_invite_user_to_chat(text_data_json)
            elif what_type == 'block_user':
                await self.handle_block_user(text_data_json)
            elif what_type == 'get_blocked_by_user':
                await self.handle_get_blocked_by_user(text_data_json)
            elif what_type == 'get_blocked_user':
                await self.handle_get_blocked_user(text_data_json)
            elif what_type == 'unblock_user':
                await self.handle_unblock_user(text_data_json)
            elif what_type == 'get_avatar':
                await self.handle_get_avatar(text_data_json)
            else:
                print('IS SOMETHING ELSE')


    async def controlGameRequests(self, text_data_json, what_type):
        game_id = text_data_json["data"]["game_id"]
        self.game_group_id = 'group_%s' % game_id

        print(self.game_group_id)
        print(self.user)
        print('______________\n')

        await self.init_game_struct()

        await self.channel_layer.group_add(
            self.game_group_id,
            self.channel_name
        )
        if what_type == 'send_game_scene':
            self.key_code = text_data_json["data"]["key_code"]
            self.prev_pos = text_data_json["data"]["prev_pos"]
            await self.handle_send_game_scene()
        elif what_type == 'send_init_game':
            self.game_id = game_id
            await self.handle_send_init_game()
        elif what_type == 'send_ball_update':
            self.game_id = game_id
            await self.handle_send_ball_update()
        elif what_type == 'send_request_invites':
            self.game_id = game_id
            await self.handle_send_invites()
        else:
            print('IS SOMETHING ELSE')


# ---------------------------- HANDLE FUNCTIONS ---------------------------

# ---------------------------- DATABASE FUNCTIONS ----------------------------

    @database_sync_to_async
    def group_exists(self, group_name):
        channel_layer = get_channel_layer()
        return channel_layer.group_exists(group_name)

