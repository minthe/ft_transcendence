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
# - Endpoint: game/user/{user_id}/
# - Method:   POST
# - Payload:  username:string, avatar:string
@require_POST
def createUser(request, user_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        avatar = data.get('avatar')

        # check if user already exists
        user_exist = MyUser.objects.filter(user_id=user_id).exists()
        if user_exist:
            return JsonResponse({}, status=409)

        new_user = MyUser()
        new_user.user_id = user_id
        new_user.name = username
        new_user.avatar = avatar
        new_user.age = 69
        new_user.save()

        return JsonResponse({}, status=200)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({}, status=500)


# Update Avatar:
# - Endpoint: game/user/{user_id}/avatar/
# - Method:   PUT
# - Payload:  avatar:string
@require_http_methods(["PUT"])
def updateAvatar(request, user_id):
    try:
        return JsonResponse({}, status=501)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({}, status=500)


# Update game alias:
# - Endpoint: game/user/{user_id}/alias/
# - Method:   PUT
# - Payload:  alias:string
@require_http_methods(["PUT"])
def updateAlias(request, user_id):
    try:
        return JsonResponse({}, status=501)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({}, status=500)



@csrf_exempt
@require_POST
def checkUserCredentials(request):#TODO Marie: user user_id to get user
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        # enable2FA boolean | later get this from db instead of frontend
        enable2FA:bool = data.get('enable2FA')
        email_to = data.get('email')

        user_exist_check = MyUser.objects.filter(name=username).exists()
        if not user_exist_check:
            return JsonResponse({}, status=404)
        user_object = MyUser.objects.get(name=username)
        if password == user_object.password:
            if enable2FA:
                send_email_to_user(user_object, email_to)
            return JsonResponse({'user_id': user_object.user_id, 'twoFactorAuth': enable2FA}, status=200)
        else:
            return JsonResponse({}, status=401)  # wrong credentials
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({}, status=500)

def send_email_to_user(user, email_to):
    email_from = settings.EMAIL_HOST_USER
    code = user.generate_verification_code()
    send_mail(
        'Your 2FA Code',
        f'Your 2FA code is: {code}',
        email_from,
        [email_to],
        fail_silently=False,
    )

def verifyTwoFactorCode(request, code, username):
    try:
        user_exists = MyUser.objects.filter(name=username).exists()
        if not user_exists:
            return JsonResponse({'message': 'User not found'}, status=404)
        user_instance = MyUser.objects.get(name=username)
        if user_instance.verify_verification_code(code):
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({'message': 'Invalid or expired verification code'}, status=400)
    except Exception as e:
        print("in verifyTwoFactorCode: ", e)
        return JsonResponse({}, status=500)



from django.core.mail import send_mail
@csrf_exempt
@require_POST
def createAccount(request):#TODO Marie: user user_id to get user
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user_exist = MyUser.objects.filter(name=username).exists()
        if user_exist:
            return JsonResponse({}, status=409)
        user_data = {
            "name": username,
            "password": password,
            "age": 69
        }
        new_user = MyUser(**user_data)
        new_user.save()
        user_instance = MyUser.objects.get(name=username)
        return JsonResponse({'user_id': user_instance.user_id}, status=200)
    except Exception as e:
        print("in createAccount: ", e)
        return JsonResponse({}, status=500)


@require_POST
@jwt.token_required
def uploadAvatar(request, username):
    try:
        print("REQUEST: ", request.headers)

        print('username: ', username)
        user_exist = MyUser.objects.filter(name=username).exists()
        if not user_exist:
            return JsonResponse({}, status=409)

        if request.method == 'POST':
            user_instance = MyUser.objects.get(name=username)
            avatar_file = request.FILES.get('avatar')
            print('response file: ', avatar_file)
            if avatar_file:
                user_instance.avatar = avatar_file
                user_instance.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        return JsonResponse({}, status=500)


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
