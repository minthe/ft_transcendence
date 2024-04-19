from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import random
import string


# inherits from "models.Model" which means it's a database model
class MyUser(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    name = models.CharField("name", max_length=100)
    password = models.CharField("password", max_length=100)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    chats = models.ManyToManyField('Chat', blank=True)
    new_matches = models.ManyToManyField('Game', blank=True)
    blockedBy = models.ManyToManyField('self', blank=True, symmetrical=False)
    # gameAlias = models.CharField("gameAlias", max_length=100) #Julien changed


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
    # hostName = models.CharField("hostName", max_length=100) #Julien changed
    # guestName = models.CharField("guestName", max_length=100) #Julien changed

class Tournament(models.Model):
    # quarterMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    quarterMatch = ArrayField(models.IntegerField(), blank=True, default=list)
    semiMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    finalMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)