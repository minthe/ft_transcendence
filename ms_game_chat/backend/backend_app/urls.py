from django.urls import path
from . import views
from . import utils
# from .views import updateUserPassword

urlpatterns = [
    path('', views.goToFrontend),  # happens when user enters backend port

    # LOGIN/REGISTER
    # 'login'
    path('user/login/', views.checkUserCredentials),

    # 'register'
    path('user/register/', views.createAccount),

    # CHAT
    # 'user/avatar'
    path('game/avatar/<str:username>/', views.uploadAvatar),

    # GAME
    # 'game/create'
    path('game/create/<str:username>/<str:invited_username>', views.createGame),

    # 'game/invite'
    path('game/invite/<str:username>/<int:game_id>/<str:guest_user_name>/', views.inviteUserToGame),

    # 'game/render/invites'
    path('game/render/invites/<str:username>/', views.renderInvites),

]
