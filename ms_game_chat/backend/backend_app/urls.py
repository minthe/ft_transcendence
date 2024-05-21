from django.urls import path
from . import views

urlpatterns = [

    # REQUESTS FROM MS_AUTH
    path('game/user', views.createUser),
    path('game/user/avatar', views.updateAvatar),
    path('game/user/alias', views.updateAlias),

    # GAME
    path('game/create/<str:username>/<str:invited_username>', views.createGame),
    path('game/invite/<str:username>/<int:game_id>/<str:guest_user_name>/', views.inviteUserToGame),
    path('game/render/invites/<str:username>/', views.renderInvites),
]
