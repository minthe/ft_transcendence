from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings
from ft_jwt.ft_jwt import FT_JWT
import json
from django.views.decorators.csrf import csrf_exempt

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

        # check if user already exists
        if not MyUser.objects.filter(user_id=jwt_user_id).exists():
            return JsonResponse({'message': 'User does not exist'}, status=409)

        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        avatar = data.get('avatar')

        new_user = MyUser()
        new_user.user_id = jwt_user_id
        new_user.name = username
        new_user.avatar = avatar
        new_user.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)

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
        return JsonResponse({'message': 'Not implemented yet'}, status=501)
        data = json.loads(request.body.decode('utf-8'))
        alias = data.get('alias')

        if not MyUser.objects.filter(user_id=jwt_user_id).exists():
            return JsonResponse({'message': 'User does not exist'}, status=404)

        user_instance = MyUser.objects.get(user_id=jwt_user_id)
        return
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'message': e}, status=500)


######### GAMEEEEEEEEEEEEEEEEEEEE ######### kristinas kingdom:


from django.http import JsonResponse
from backend_app.models import Game, MyUser

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
