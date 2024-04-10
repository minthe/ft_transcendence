from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# inherits from "models.Model" which means it's a database model
class MyUser(models.Model):
    user_id = models.AutoField(primary_key=True) # delete this and use next line, as soon as we get user in backend from ms_auth
    # user_id = models.IntegerField(default=-1, null=False, blank=False)
    name = models.CharField("name", max_length=100)
    password = models.CharField("password", max_length=100)
    age = models.IntegerField("age")
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    chats = models.ManyToManyField('Chat', blank=True)
    new_matches = models.ManyToManyField('Game', blank=True)
    blockedBy = models.ManyToManyField('self', blank=True, symmetrical=False)

class Chat(models.Model):
    chatName = models.CharField("chatName", max_length=100)
    isPrivate = models.BooleanField(default=False)
    messages = models.ManyToManyField('Message', blank=True)


class Message(models.Model):
    senderId = models.CharField("senderId", max_length=50)
    sender = models.CharField(max_length=50)
    text = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(default=timezone.now)

    def formatted_timestamp(self):
        return self.timestamp.strftime('%H:%M %d.%m.%Y')

class Game(models.Model):
    hostId = models.CharField("hostId", max_length=69, default=None, blank=True, null=True)
    guestId = models.CharField("guestId", max_length=69, default=None, blank=True, null=True)

class Tournament(models.Model):
    # quarterMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    quarterMatch = ArrayField(models.IntegerField(), blank=True, default=list)
    semiMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    finalMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)