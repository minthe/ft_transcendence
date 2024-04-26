from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings
from ft_jwt.ft_jwt import FT_JWT
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from backend_app.models import Game, MyUser, Chat, Message


jwt = FT_JWT(settings.JWT_SECRET)

def goToFrontend(request):
    return render(request, 'goToFrontend.html')

# Create new user:
# - Endpoint: game/user/
# - Method:   POST
# - Payload:  username:string, avatar:string
@require_POST
@jwt.token_required
def createUser(request):
    try:
        jwt_user_id = request.user_id
        if MyUser.objects.filter(user_id=jwt_user_id).exists():
            print(f"User {jwt_user_id} already exists")
            return JsonResponse({'message': 'User already exists'}, status=409)
        if jwt_user_id == 1:
            delete_later = "USER ID 1 SHOULD BE FOR CHATBOT, VALENTIN PLS FIX"
            print(delete_later)
            return JsonResponse({'message', delete_later}, status=500)
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
        print(f"FAILED TO CREATE CHAT BOT: {response}")
        raise Exception("Failed to create Chat Bot: ", response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)

from django.utils import timezone

def createChatWithChatBot(user_id):
    try:
        chat_name = 'CHAT_BOT'
        if not MyUser.objects.filter(name=chat_name).exists():
            delete_later = createChatBot(chat_name)
            if delete_later != 'ok':
                JsonResponse({'message': delete_later}, status=499) # delete later, debug
        chat_bot_instance = MyUser.objects.get(name=chat_name)
        user_instance = MyUser.objects.get(user_id=user_id)
        new_chat = Chat.objects.create(chatName=chat_name, isPrivate=True)
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
        return "User does not exist 2"
    except Exception as e:
        return str(e)


def createChatBot(chat_name):
    if MyUser.objects.filter(user_id=1).exists(): # delete later when chatbot works
        return "CHATBOT DOES NOT EXIST YET BUT USER ID 1 IS NOT FREE, MARIE & VALENTIN PLS FIX"
    chat_bot = MyUser()
    chat_bot.user_id = 1
    chat_bot.name = chat_name
    chat_bot.avatar = 'https://pics.craiyon.com/2024-02-12/aHmqcreDRDasUbg-rJVcCA.webp'
    chat_bot.alias = chat_name
    chat_bot.save()
    return "ok"

# Update Avatar:
# - Endpoint: game/user/avatar/
# - Method:   PUT
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

# Update game alias:
# - Endpoint: game/user/alias/
# - Method:   PUT
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
        setattr(user_instance, 'gameAlias', alias)
        user_instance.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)


######### GAMEEEEEEEEEEEEEEEEEEEE ######### kristinas kingdom:


from django.http import JsonResponse

def createGame(request, username, invited_username):
    try:
        print(f"Entering createGameroom function with username: {username}")

        # Get the user instances
        user = MyUser.objects.get(name=username)
        invited_user = MyUser.objects.get(name=invited_username)

        # Check if a game already exists with the given pair of users in new_matches
        existing_game = user.new_matches.filter(hostId=invited_username, guestId=username).exists()
        if existing_game:
            return JsonResponse({"error": "A game already exists with these users"}, status=400)

        # Check if the users are reversed (host and guest swapped) in new_matches
        existing_game_reversed = invited_user.new_matches.filter(hostId=username, guestId=invited_username).exists()
        if existing_game_reversed:
            return JsonResponse({"error": "A game already exists with these users"}, status=400)

        # If no existing game found in new_matches, create a new game
        new_gameroom = Game.objects.create(hostId=username, guestId=invited_username)
        print(f"11111")
        new_gameroom.save()

        # Add the new game to the new_matches field of both users
        user.new_matches.add(new_gameroom)
        invited_user.new_matches.add(new_gameroom)
        print(f"new_matches")
        print(user.new_matches.all())

        return JsonResponse({"message": "Gameroom was created successfully", "id": new_gameroom.id,})
        # "host_name": new_gameroom.hostId, "guest_name": new_gameroom.guestId
    except MyUser.DoesNotExist:
        return JsonResponse({"error": "Invalid username"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def inviteUserToGame(request, username, game_id, guest_user_name):
    try:
        print(f"backend invite user")
        guest_user_exists = MyUser.objects.filter(name=guest_user_name).exists()
        if not guest_user_exists:
            return JsonResponse({'error': 'User you want to invite doesnt exists'}, status=404)

        # get instance of both users
        host_exists = MyUser.objects.filter(name=username)
        if not host_exists:
            return JsonResponse({"error": "User does not exist 1"}, status=404)
        host_user = MyUser.objects.get(name=username)

        guest_user = MyUser.objects.get(name=guest_user_name)

        # get instance of chat that the user is inviting the other user to
        # game = host_user.new_matches.get(id=game_id)
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
        print(f"Entering renderInvites function with username: {username}")
        user = MyUser.objects.get(name=username)
        print(f"22222")
        print(f" {user}")

        game_sessions = user.new_matches.all()
        # test_var = game_sessions.get(id=1)
        # usernames = []
        # for session in game_sessions:
        #     usernames.append(session.username)

        # game_sessions = user.new_matches.get(id=2)
        # game_sessions = Game.objects.all()

        print(f"333333")
        print(f" {game_sessions}")
        # print(f"444444")
        # print(f" {test_var}")

        # return render(request, 'openGameSessions.html', {'game_sessions': game_sessions})
        return render(request, 'openGameSessions.html', {'game_sessions': game_sessions})

    # except ValueError:
    #     return JsonResponse({"error": "Invalid username"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# def renderDisplay(request, game_id)
