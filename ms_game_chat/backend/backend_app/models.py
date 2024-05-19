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
    avatar = models.CharField(max_length=1000, null=True)
    alias = models.CharField(max_length=1000, null=True)
    chats = models.ManyToManyField('Chat', blank=True)
    blockedBy = models.ManyToManyField('self', blank=True, symmetrical=False)
    new_matches = models.ManyToManyField('Game', related_name='new_matches', blank=True)
    old_matches = models.ManyToManyField('Game', related_name='old_matches', blank=True)
    tourns = models.ManyToManyField('Tournament', related_name='passed_turns', blank=True)
    # gameAlias = models.CharField("gameAlias", max_length=100) #Julien changed


class Chat(models.Model):
    chatName = models.CharField("chatName", max_length=100)
    isPrivate = models.BooleanField(default=False)
    messages = models.ManyToManyField('Message', blank=True)
    is_read = models.BooleanField(default=True)

class Message(models.Model):
    senderId = models.CharField("senderId", max_length=50)
    sender = models.CharField(max_length=50)
    text = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(default=timezone.now)

    def formatted_timestamp(self):
        return self.timestamp.strftime('%H:%M %d.%m.%Y')

class Game(models.Model):
    hostId = models.CharField("hostId", max_length=100, default=None, blank=True, null=True)
    guestId = models.CharField("guestId", max_length=100, default=None, blank=True, null=True)
    winnerId = models.CharField("winnerId", max_length=100, default=None, blank=True, null=True)
    loserId = models.CharField("loserId", max_length=100, default=None, blank=True, null=True)
    tournId = models.IntegerField("tournId", default=None, blank=True, null=True)
    stage = models.CharField("stage", max_length=100)
    date = models.DateTimeField(default=timezone.now)
    # hostName = models.CharField("hostName", max_length=100) #Julien changed
    # guestName = models.CharField("guestName", max_length=100) #Julien changed

class Tournament(models.Model):
    semiMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    finalMatch = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    hostId = models.CharField("hostId", max_length=100, default=None, blank=True, null=True)
    active_matches = models.ManyToManyField('Game', related_name='active_matches', blank=True)
    passed_matches = models.ManyToManyField('Game', related_name='passed_matches', blank=True)
    winnerId = models.CharField("winnerId", max_length=100, default=None, blank=True, null=True)
    status = models.CharField("status", max_length=100, default="active")

