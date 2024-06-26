import json
from channels.db import database_sync_to_async
from backend_app.models import MyUser, Chat, Message, Game
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class _Chat:
# ---------- HANDLE FUNCTIONS ---------------------------------------

    async def handle_send_current_users_chats(self, text_data_json):
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if user_id == -1: return
        users_chats = await self.get_users_chats(user_id)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.current.users.chats',
                'data': {
                    'user_id': user_id,
                    'users_chats': users_chats,
                },
            }
        )

    async def handle_create_new_public_chat(self, text_data_json):
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if user_id == -1: return
        chat_name = text_data_json["data"]["chat_name"]
        is_private = text_data_json["data"]["isPrivate"]
        info = await self.createChat(user_id, chat_name, is_private)
        await self.send(text_data=json.dumps({
            'type': 'created_chat',
            'chat_id': info["chat_id"],
            'message': info["message"]
        }))

    async def handle_create_new_private_chat(self, text_data_json):
        # chat_name IS the others users name!!
        chat_name = text_data_json["data"]["chat_name"]
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if user_id == -1: return
        info = await self.createPrivateChat(user_id, chat_name)
        others_user_id = await self.get_id_with_name(chat_name)
        others_user_channel_name = await self.get_channel_name_with_id(others_user_id)
        if others_user_channel_name is not None:
            await self.channel_layer.group_add(self.my_group_id, others_user_channel_name)
            other_users_chats = await self.get_users_chats(others_user_id)
            await self.channel_layer.group_send(
                self.my_group_id,
                {
                    'type': 'send.current.users.chats',
                    'data': {
                        'user_id': others_user_id,
                        'users_chats': other_users_chats,
                    },
                }
            )
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.new.private.chat.info',
                'data': {
                    'message': info
                },
            }
        )

    async def handle_invite_user_to_chat(self, text_data_json):
        chat_id = self.get_and_check_id(text_data_json["data"]["chat_id"])
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        invited_user_name = self.get_and_check_name(text_data_json["data"]["invited_user_name"])
        if chat_id == -1 or user_id == -1 or invited_user_name == -1: return
        info = await self.inviteUserToChat(user_id, chat_id, invited_user_name)
        others_user_id = await self.get_id_with_name(invited_user_name)
        others_user_channel_name = await self.get_channel_name_with_id(others_user_id)
        if others_user_channel_name is not None:
            await self.channel_layer.group_add(self.my_group_id, others_user_channel_name)
            other_users_chats = await self.get_users_chats(others_user_id)
            await self.channel_layer.group_send(
                self.my_group_id,
                {
                    'type': 'send.current.users.chats',
                    'data': {
                        'user_id': others_user_id,
                        'users_chats': other_users_chats,
                    },
                }
            )
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.invited.user.to.chat.info',
                'data': {
                    'message': info
                },
            }
        )

    async def handle_block_user(self, text_data_json):
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        user_to_block = self.get_and_check_name(text_data_json["data"]["user_to_block"])
        if user_id == -1 or user_to_block == -1: return
        response = await self.block_user(user_id, user_to_block)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.blocked.user.info',
                'data': {
                    'status': response["status"],
                    'user_id': user_id,
                    'other_user_name': user_to_block
                },
            }
        )

    async def handle_get_blocked_by_user(self, text_data_json):
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if user_id == -1: return
        response = await self.get_blocked_by_user(user_id)
        await self.send(text_data=json.dumps({
            'type': 'blocked_by_user',
            'blocked_by': response["blocked_by"],
            'status': response["status"],
            'user_id': user_id,
        }))


    async def handle_unblock_user(self, text_data_json):
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        user_to_unblock = self.get_and_check_name(text_data_json["data"]["user_to_unblock"])
        if user_id == -1 or user_to_unblock == -1: return
        response = await self.unblock_user(user_id, user_to_unblock)
        await self.channel_layer.group_send(
            self.my_group_id,
            {
                'type': 'send.unblocked.user.info',
                'data': {
                    'status': response["status"],
                    'user_id': user_id,
                    'other_user_name': user_to_unblock
                },
            }
        )

    async def handle_get_blocked_user(self, text_data_json):
        user_id = self.get_and_check_id(text_data_json["data"]["user_id"])
        if user_id == -1: return
        response = await self.get_blocked_user(user_id)
        await self.send(text_data=json.dumps({
            'type': 'blocked_user',
            'blocked_user': response["blocked_user"],
            'status': response["status"],
            'user_id': user_id,
        }))

    async def handle_new_tournament_chatbot(self, text_data_json):
        invited_user_name = self.get_and_check_name(text_data_json["data"]["invited_user_name"])
        current_user_name = self.get_and_check_name(text_data_json["data"]["current_user_name"])
        if invited_user_name == -1 or current_user_name == -1: return
        invited_user_id = await self.get_id_with_name(invited_user_name)
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.inform.chatbot',
                'data': {
                    'message': 'ok',
                    'user_id': invited_user_id,
                    'other_user_name': current_user_name
                },
            }
        )

    async def handle_save_chatbot_message(self, text_data_json):
        other_user_name = self.get_and_check_name(text_data_json["data"]["other_user_name"])
        current_user_name = self.get_and_check_name(text_data_json["data"]["current_user_name"])
        if other_user_name == -1 or current_user_name == -1: return
        message = "Hey, " + other_user_name + " invited you to a tournament! Go to the Game interface to play."
        response_message = await self.create_message_chatbot(current_user_name, message)
        await self.send(text_data=json.dumps({
            'type': 'message_save_success_bot',
            'message': response_message
        }))

    async def handle_inform_chatbot_new_game(self, text_data_json):
        if (text_data_json["data"]["game_type"] == 'semi_final'):
            await self.handle_inform_chatbot_new_game_semifinal(text_data_json)
        elif (text_data_json["data"]["game_type"] == 'final'):
            await self.handle_inform_chatbot_new_game_final(text_data_json)

    async def handle_inform_chatbot_new_game_semifinal(self, text_data_json):
        user_one_id = text_data_json["data"]["user_one_id"]
        user_one_name = text_data_json["data"]["user_one_name"]
        user_two_id = text_data_json["data"]["user_two_id"]
        user_two_name = text_data_json["data"]["user_two_name"]
        user_three_id = text_data_json["data"]["user_three_id"]
        user_three_name = text_data_json["data"]["user_three_name"]
        user_four_id = text_data_json["data"]["user_four_id"]
        user_four_name = text_data_json["data"]["user_four_name"]
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.inform.chatbot.new.game',
                'sender': text_data_json["data"]["user_id"],
                'data': {
                    'game_type': 'semi_final',
                    'user_one_id': user_one_id,
                    'user_one_name': user_one_name,
                    'user_two_id': user_two_id,
                    'user_two_name': user_two_name,
                    'user_three_id': user_three_id,
                    'user_three_name': user_three_name,
                    'user_four_id': user_four_id,
                    'user_four_name': user_four_name,
                },
            }
        )

    async def handle_inform_chatbot_new_game_final(self, text_data_json):
        user_one_id = text_data_json["data"]["user_one_id"]
        user_one_name = text_data_json["data"]["user_one_name"]
        user_two_id = text_data_json["data"]["user_two_id"]
        user_two_name = text_data_json["data"]["user_two_name"]
        await self.channel_layer.group_send(
            'channel_zer0',
            {
                'type': 'send.inform.chatbot.new.game',
                'sender': text_data_json["data"]["user_id"],
                'data': {
                    'game_type': 'final',
                    'user_one_id': user_one_id,
                    'user_one_name': user_one_name,
                    'user_two_id': user_two_id,
                    'user_two_name': user_two_name,
                },
            }
        )

    async def handle_send_chatbot_message_new_game(self, text_data_json):
        if (text_data_json["data"]["game_type"] == 'semi_final'):
            await self.handle_send_chatbot_message_new_game_semifinal(text_data_json)
        elif (text_data_json["data"]["game_type"] == 'final'):
            await self.handle_send_chatbot_message_new_game_final(text_data_json)


    async def handle_send_chatbot_message_new_game_semifinal(self, text_data_json):
        user_id = text_data_json["data"]["user_id"]
        user_one_id = text_data_json["data"]["user_one_id"]
        user_two_id = text_data_json["data"]["user_two_id"]
        user_three_id = text_data_json["data"]["user_three_id"]
        user_four_id = text_data_json["data"]["user_four_id"]
        if user_id == user_one_id:
            opponent = text_data_json["data"]["user_two_name"]
        elif user_id == user_two_id:
            opponent = text_data_json["data"]["user_one_name"]
        elif user_id == user_three_id:
            opponent = text_data_json["data"]["user_four_name"]
        elif user_id == user_four_id:
            opponent = text_data_json["data"]["user_three_name"]
        current_user_name = await self.get_name_with_id(user_id)
        message = "Yoooo, " + opponent + " is waiting for you to play the first match in the tournament against you. If you win this game you will go in the final round!"
        response_message = await self.create_message_chatbot(current_user_name, message)
        await self.send(text_data=json.dumps({
            'type': 'message_save_success_bot',
            'message': response_message
        }))

    async def handle_send_chatbot_message_new_game_final(self, text_data_json):
        user_id = text_data_json["data"]["user_id"]
        user_one_id = text_data_json["data"]["user_one_id"]
        user_two_id = text_data_json["data"]["user_two_id"]
        if user_id == user_one_id:
            opponent = text_data_json["data"]["user_two_name"]
        elif user_id == user_two_id:
            opponent = text_data_json["data"]["user_one_name"]
        current_user_name = await self.get_name_with_id(user_id)
        message = "SHEEEESH, " + opponent + " is waiting for you to play the LAST and FINAL match in the tournament against you!! If you win this game you are the WINNER OF THE TOURNAMENT!"
        response_message = await self.create_message_chatbot(current_user_name, message)
        await self.send(text_data=json.dumps({
            'type': 'message_save_success_bot',
            'message': response_message
        }))


# ---------- SEND FUNCTIONS ---------------------------------------
    async def send_current_users_chats(self, event):
        await self.send(text_data=json.dumps({
            'type': 'current_users_chats',
            'user_id': event['data']['user_id'],
            'users_chats': event['data']['users_chats']
        }))

    async def send_inform_chatbot(self, event):
        await self.send(text_data=json.dumps({
            'type': 'inform_chatbot',
            'user_id': event['data']['user_id'],
            'other_user_name': event['data']['other_user_name']
        }))

    async def send_user_left_chat(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_left_chat_info',
            'message': event['data']['message'],
        }))

    async def send_new_chat_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'created_chat',
            'message': event['data']['message'],
        }))

    async def send_new_private_chat_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'created_private_chat',
            'message': event['data']['message'],
        }))

    async def send_invited_user_to_chat_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'invited_user_to_chat',
            'message': event['data']['message'],
        }))

    async def send_blocked_user_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'blocked_user_info',
        }))

    async def send_blocked_user(self, event):
        await self.send(text_data=json.dumps({
            'type': 'blocked_user',
            'blocked_by': event['data']['blocked_by'],
        }))

    async def send_unblocked_user_info(self, event):
        await self.send(text_data=json.dumps({
            'type': 'unblocked_user_info',
            'status': event['data']['status'],
            'user_id': event['data']['user_id'],
        }))

    async def send_inform_chatbot_new_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'inform_chatbot_new_game',
            'sender': event["sender"],
            'data': event['data']
        }))
# ---------- DATABASE REQUEST FUNCTIONS -----------------------------

    @database_sync_to_async
    def get_users_chats(self, user_id):
        if not MyUser.objects.filter(user_id=user_id).exists():
            print("user id not found in get_users_chats")
            return
        user_instance = MyUser.objects.get(user_id=user_id)
        all_chats = user_instance.chats.all()
        user_chats = []
        for chat in all_chats:
            chat_name = self.getChatName(chat, user_id)
            user_chats.append({
                'chat_id': chat.id,
                'chat_name': chat_name,
                'private_chat_names': self.getPrivateChatNames(chat, user_id),
                'last_message': self.get_last_message_in_chat(chat.id),
                'isPrivate': chat.isPrivate,
                'avatar': self.getAvatar(chat_name),
                'is_read': self.get_is_read_stat(chat.id, user_id)
            })
        return user_chats

    @database_sync_to_async
    def createChat(self, user_id, chat_name, is_private):
        try:
            if Chat.objects.filter(chatName=chat_name).exists():
                return {'chat_id': -1, 'message': 'Chat already exists'}
            new_chat = Chat.objects.create(chatName=chat_name, isPrivate=is_private)
            user_instance = MyUser.objects.get(user_id=user_id)
            user_instance.chats.add(new_chat.id)
            new_chat.save()
            user_instance.save()
            chat_instance = Chat.objects.get(chatName=chat_name)
            return {'chat_id': chat_instance.id, 'message': 'ok'}
        except ValueError:
            return {'chat_id': -1, 'message': "Invalid user ID"}
        except Exception as e:
            return str(e)

    @database_sync_to_async
    def createPrivateChat(self, user_id, chat_name):
        try:
            # chat_name should be the user we create a chat with
            if not MyUser.objects.filter(name=chat_name).exists():
                return 'User does not exist'
            user_instance = MyUser.objects.get(user_id=user_id)
            if chat_name == user_instance.name:
                return 'Sorry, you can not be in a chat with yourself :('
            # Filter all private chats that the user is part of
            private_chats = Chat.objects.filter(isPrivate=True, myuser__user_id=user_id)
            if private_chats.filter(myuser__name=chat_name):
                return "You are already in a private chat with this user"
            new_chat = Chat.objects.create(chatName=chat_name, isPrivate=True)
            current_user_instance = MyUser.objects.get(user_id=user_id)
            other_user_instance = MyUser.objects.get(name=chat_name)
            current_user_instance.chats.add(new_chat.id)
            current_user_instance.save()
            other_user_instance.chats.add(new_chat.id)
            other_user_instance.save()
            new_chat.save()
            return "ok"
        except ValueError:
            return "User does not exist 2"
        except Exception as e:
            return str(e)

    @database_sync_to_async
    def get_id_with_name(self, user_name):
        try:
            user_instance = MyUser.objects.get(name=user_name)
            user_id = user_instance.user_id
            return user_id
        except Exception as e:
            return -1

    @database_sync_to_async
    def get_name_with_id(self, id):
        try:
            user_instance = MyUser.objects.get(user_id=id)
            name = user_instance.name
            return name
        except Exception as e:
            return -1

    @database_sync_to_async
    def get_chat_id_with_name(self, chat_name):
        try:
            chat_instance = Chat.objects.get(name=chat_name)
            chat_id = chat_instance.chat_id
            return chat_id
        except Exception as e:
            print(f"something wrong in get_chat_id_with_name: {e}")
            return -1

    @database_sync_to_async
    def inviteUserToChat(self, user_id, chat_id, invited_user):
        try:
            if not MyUser.objects.filter(name=invited_user).exists():
                return 'User you want to invite doesnt exists'
            inviting_user = MyUser.objects.get(user_id=user_id)
            invited_user = MyUser.objects.get(name=invited_user)
            chat = inviting_user.chats.get(id=chat_id)
            invited_user.chats.add(chat)
            return 'ok'
        except invited_user.DoesNotExist:
            return "User does not exist"
        except Exception as e:
            return str(e)

    @database_sync_to_async
    def block_user(self, user_id, user_to_block):
        current_user_exists = MyUser.objects.filter(user_id=user_id).exists()
        other_user_exists = MyUser.objects.filter(name=user_to_block).exists()
        if not current_user_exists or not other_user_exists:
            return {'status': 404, 'blocked_by': None}
        current_user_instance = MyUser.objects.get(user_id=user_id)
        other_user_instance = MyUser.objects.get(name=user_to_block)
        # create blocked_by field in instance of user_to_block and add there the name of instance user_id
        # Check if the other user is already blocked
        if current_user_instance in other_user_instance.blockedBy.all():
            # User is already blocked, return a response or handle accordingly
            return {'status': 409, 'blocked_by': None}
        # Block the other user
        other_user_instance.blockedBy.add(current_user_instance)
        other_user_instance.save()
        return {'status': 200}

    @database_sync_to_async
    def unblock_user(self, user_id, user_to_unblock):
        current_user_exists = MyUser.objects.filter(user_id=user_id).exists()
        other_user_exists = MyUser.objects.filter(name=user_to_unblock).exists()
        if not current_user_exists or not other_user_exists:
            return {'status': 404, 'unblocked_by': None}
        current_user_instance = MyUser.objects.get(user_id=user_id)
        other_user_instance = MyUser.objects.get(name=user_to_unblock)
        if current_user_instance in other_user_instance.blockedBy.all():
            other_user_instance.blockedBy.remove(current_user_instance)
            other_user_instance.save()
            return {'status': 200}
        return {'status': 409, 'unblocked_by': None}  # 'User already blocked'

    @database_sync_to_async
    def get_blocked_by_user(self, user_id):
        if not MyUser.objects.filter(user_id=user_id).exists():
            print("user id not found in get_blocked_by_user")
            return
        user_instance = MyUser.objects.get(user_id=user_id)
        blocked_by_names = user_instance.blockedBy.values_list('name', flat=True)
        blocked_by_names_list = list(blocked_by_names)
        return {'status': 200, 'blocked_by': blocked_by_names_list}

    @database_sync_to_async
    def get_blocked_user(self, user_id):
        if not MyUser.objects.filter(user_id=user_id).exists():
            print("user id not found in get_blocked_user")
            return
        current_user = MyUser.objects.get(user_id=user_id)
        users_blocking_current_user = MyUser.objects.filter(blockedBy=current_user)
        blocked_by_current_user_names = users_blocking_current_user.values_list('name', flat=True)
        blocked_by_names_list = list(blocked_by_current_user_names)
        return {'status': 200, 'blocked_user': blocked_by_names_list}

# ---------- UTILS FUNCTIONS ----------------------------------------

    def getChatName(self, chat_instance, user_id):
        if not chat_instance.isPrivate:
            return chat_instance.chatName
        # if chat is private, need to figure out name of chat user that is not current user
        chat_id = chat_instance.id
        users_in_chat = MyUser.objects.filter(chats__id=chat_id)
        current_user_instance = MyUser.objects.get(user_id=user_id)
        current_user = current_user_instance.name
        # get other users name
        for user in users_in_chat:
            if not current_user == user.name:
                return user.name
        return 'Unexpected Error in getChatName()'

    def getPrivateChatNames(self, chat_instance, user_id):
        if not chat_instance.isPrivate:
            return None
        # if chat is private, need to figure out name of chat user that is not current user
        chat_id = chat_instance.id
        users_in_chat = MyUser.objects.filter(chats__id=chat_id)
        chat_names_list = [user.name for user in users_in_chat]
        return chat_names_list

    def get_last_message_in_chat(self, chat_id):
        try:
            chat_instance = Chat.objects.get(id=chat_id)
            last_message = chat_instance.messages.order_by('-timestamp').first()
            if last_message:
                return {'text': last_message.text, 'time': last_message.formatted_timestamp(), 'status': 'ok'}
        except ObjectDoesNotExist:
            print("Chat does not exist.")
        return {'text': '', 'time': '0', 'status': 'Not found'}

    async def get_channel_name_with_id(self, user_id):
        for channel in self.channels:
            if channel['user_id'] == str(user_id):
                return channel['channel_name']
        return None

    def getAvatar(self, chat_name):
        if not MyUser.objects.filter(name=chat_name).exists():
            return None
        user_instance = MyUser.objects.get(name=chat_name)
        avatar_url = user_instance.avatar if user_instance.avatar else None
        if self.is_valid_url(avatar_url):
            result = str(avatar_url) if avatar_url else None
        else:
            result = str(avatar_url) if avatar_url else None # doesnt work if avatar is url
        return result

    def is_valid_url(self, url):
        validator = URLValidator()
        try:
            validator(url)
            return True
        except ValidationError:
            return False

    def get_is_read_stat(self, chat_id, user_id):
        user_instance = MyUser.objects.get(user_id=user_id)
        chat_instance = user_instance.chats.get(id=chat_id)
        is_read = chat_instance.is_read
        return is_read
