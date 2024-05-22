from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings
from ft_jwt.ft_jwt import FT_JWT
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from backend_app.models import Game, MyUser, Chat, Message
from django.utils import timezone
from django.http import JsonResponse


jwt = FT_JWT(settings.JWT_SECRET)

# - Endpoint: game/user/
# - Payload:  username:string, avatar:string
@require_POST
@jwt.token_required
def createUser(request):
    try:
        jwt_user_id = request.user_id
        if MyUser.objects.filter(user_id=jwt_user_id).exists():
            return JsonResponse({'message': 'User already exists'}, status=409)
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        avatar = data.get('avatar')
        new_user = MyUser()
        new_user.user_id = jwt_user_id
        new_user.name = username
        new_user.avatar = avatar
        new_user.alias = username
        new_user.save()
        response = createChatWithChatBot(new_user.user_id)
        if response == 'ok':
            return JsonResponse({}, status=200)
        raise Exception("Failed to create Chat Bot: ", response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)

def createChatWithChatBot(user_id):
    try:
        chat_name = 'CHAT_BOT'
        if not MyUser.objects.filter(name=chat_name).exists():
            createChatBot(chat_name)
        chat_bot_instance = MyUser.objects.get(name=chat_name)
        user_instance = MyUser.objects.get(user_id=user_id)
        new_chat = Chat.objects.create(chatName=chat_name, isPrivate=True, is_read=False)
        new_chat.save()
        user_instance.chats.add(new_chat.id)
        user_instance.save()
        chat_bot_instance.chats.add(new_chat.id)
        chat_bot_instance.save()

        # create message in chat
        specific_timestamp = timezone.now()
        text = 'Hey! I am CHAT_BOT lol'
        new_message = Message.objects.create(senderId=chat_bot_instance.user_id, sender=chat_name, text=text,
                                             timestamp=specific_timestamp)
        chat_instance = Chat.objects.get(id=new_chat.id)
        new_message.save()
        chat_instance.messages.add(new_message.id)
        return "ok"
    except ValueError:
        return "User does not exist"
    except Exception as e:
        return str(e)

def createChatBot(chat_name):
    chat_bot = MyUser()
    chat_bot.user_id = 1
    chat_bot.name = chat_name
    chat_bot.avatar = 'https://pics.craiyon.com/2024-02-12/aHmqcreDRDasUbg-rJVcCA.webp'
    chat_bot.alias = chat_name
    chat_bot.save()

# - Endpoint: game/user/avatar/
# - Payload:  avatar:string
@require_http_methods(["PUT"])
@jwt.token_required
def updateAvatar(request):
    try:
        jwt_user_id = request.user_id
        if not MyUser.objects.filter(user_id=jwt_user_id).exists():
            return JsonResponse({'message': 'User does not exist'}, status=409)
        data = json.loads(request.body.decode('utf-8'))
        avatar = data.get('avatar')
        user_instance = MyUser.objects.get(user_id=jwt_user_id)
        setattr(user_instance, 'avatar', avatar)
        user_instance.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)

# - Endpoint: game/user/alias/
# - Payload:  alias:string
@require_http_methods(["PUT"])
@jwt.token_required
def updateAlias(request):
    try:
        jwt_user_id = request.user_id
        if not MyUser.objects.filter(user_id=jwt_user_id).exists():
            return JsonResponse({'message': 'User does not exists'}, status=409)
        data = json.loads(request.body.decode('utf-8'))
        alias = data.get('alias')
        user_instance = MyUser.objects.get(user_id=jwt_user_id)
        setattr(user_instance, 'alias', alias)
        user_instance.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)


######### GAMEEEEEEEEEEEEEEEEEEEE ######### kristinas kingdom:
def createGame(request, username, invited_username):
    try:
        user = MyUser.objects.get(name=username)
        invited_user = MyUser.objects.get(name=invited_username)

        existing_game = user.new_matches.filter(hostId=invited_username, guestId=username).exists()
        if existing_game:
            return JsonResponse({"error": "A game already exists with these users"}, status=400)

        existing_game_reversed = invited_user.new_matches.filter(hostId=username, guestId=invited_username).exists()
        if existing_game_reversed:
            return JsonResponse({"error": "A game already exists with these users"}, status=400)

        new_gameroom = Game.objects.create(hostId=username, guestId=invited_username)
        new_gameroom.save()

        # Add the new game to the new_matches field of both users
        user.new_matches.add(new_gameroom)
        invited_user.new_matches.add(new_gameroom)
        return JsonResponse({"message": "Gameroom was created successfully", "id": new_gameroom.id,})
    except MyUser.DoesNotExist:
        return JsonResponse({"error": "Invalid username"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def inviteUserToGame(request, username, game_id, guest_user_name):
    try:
        guest_user_exists = MyUser.objects.filter(name=guest_user_name).exists()
        if not guest_user_exists:
            return JsonResponse({'error': 'User you want to invite doesnt exists'}, status=404)

        host_exists = MyUser.objects.filter(name=username)
        if not host_exists:
            return JsonResponse({"error": "User does not exist 1"}, status=404)
        host_user = MyUser.objects.get(name=username)
        guest_user = MyUser.objects.get(name=guest_user_name)
        game = Game.objects.get(id=game_id)

        # add chat to invited user instance
        guest_user.new_matches.add(game)
        game.guestId = guest_user.name
        game.save()
        return JsonResponse({"message": "Invite was send successfully"})
    except host_user.DoesNotExist:
        return JsonResponse({"error": "User does not exist 2"}, status=404)
    except guest_user_name.DoesNotExist:
        return JsonResponse({"error": "User does not exist 3"}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Internal Server Èrror'}, status=500)


def renderInvites(request, username):
    try:
        user = MyUser.objects.get(name=username)
        game_sessions = user.new_matches.all()
        return render(request, 'openGameSessions.html', {'game_sessions': game_sessions})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
