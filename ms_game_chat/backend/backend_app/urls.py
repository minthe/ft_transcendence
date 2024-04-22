from django.urls import path
from . import views
from . import utils
# from .views import updateUserPassword

urlpatterns = [
    path('', views.goToFrontend),  # happens when user enters backend port

    # REQUESTS FROM MS_AUTH
    path('game/user', views.createUser),
    path('game/user/avatar', views.updateAvatar),
    path('game/user/alias', views.updateAlias),

    # GAME
    path('game/create/<str:username>/<str:invited_username>', views.createGame),
    path('game/invite/<str:username>/<int:game_id>/<str:guest_user_name>/', views.inviteUserToGame),
    path('game/render/invites/<str:username>/', views.renderInvites),


    # 'game/render/display'
    # path('game/render/diyplay/<int:game_id>/', views.renderDisplay),
]
