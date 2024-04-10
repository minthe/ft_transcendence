from django.contrib import admin
from backend_app.models import MyUser, Chat, Message, Game, Tournament


admin.site.register(MyUser)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Game)
admin.site.register(Tournament)
