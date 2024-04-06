from backend_app.models import MyUser, Chat, Message
from django.http import JsonResponse
import json  # build in python module
from django.views.decorators.http import require_POST
from django.utils import timezone


@require_POST
def createMessage(request, user_id, chat_id):
    try:
        user_instance = MyUser.objects.get(id=user_id)
        specific_timestamp = timezone.now()
        data = json.loads(request.body.decode('utf-8'))
        text = data.get('text')
        new_message = Message.objects.create(sender=user_instance.name, text=text, timestamp=specific_timestamp)
        # add new_message to chat:
        chat_instance = Chat.objects.get(id=chat_id)
        chat_instance.messages.add(new_message.id)
        new_message.save()

        return JsonResponse({'message': "Message created successfully"})
    except Exception as e:
        return JsonResponse({'error': 'something big in createMessage'}, status=500)


def getChatMessages(request, chat_id):
    try:
        chat_instance = Chat.objects.get(id=chat_id)
        messages_in_chat = chat_instance.messages.all()
        message_data = [
            {
                'id': message.id,
                'sender': message.sender,
                'text': message.text,
                'timestamp': message.formatted_timestamp(),
            }
            for message in messages_in_chat
        ]
        return JsonResponse({'message_data': message_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': 'something big in createMessage'}, status=500)

def get_user_in_chat(request, chat_id):
    try:
        chat_instance = Chat.objects.get(id=chat_id)
        all_user_in_current_chat = MyUser.objects.filter(chats=chat_instance)
        user_in_chat = [
            {
                'user_name': user.name,
                'user_id': user.id
            }
            for user in all_user_in_current_chat
        ]
        return JsonResponse({'user_in_chat': user_in_chat}, status=200)
    except Exception as e:
        return JsonResponse({'error': 'something big in createMessage'}, status=500)




