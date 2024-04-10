# Generated by Django 5.0.4 on 2024-04-09 09:42

import django.contrib.postgres.fields
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostId', models.CharField(blank=True, default=None, max_length=69, null=True, verbose_name='hostId')),
                ('guestId', models.CharField(blank=True, default=None, max_length=69, null=True, verbose_name='guestId')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senderId', models.CharField(max_length=50, verbose_name='senderId')),
                ('sender', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=10000)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarterMatch', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None)),
                ('semiMatch', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None)),
                ('finalMatch', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatName', models.CharField(max_length=100, verbose_name='chatName')),
                ('isPrivate', models.BooleanField(default=False)),
                ('messages', models.ManyToManyField(blank=True, to='backend_app.message')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('password', models.CharField(max_length=100, verbose_name='password')),
                ('age', models.IntegerField(verbose_name='age')),
                ('avatar', models.FileField(blank=True, null=True, upload_to='avatars/')),
                ('blockedBy', models.ManyToManyField(blank=True, to='backend_app.myuser')),
                ('chats', models.ManyToManyField(blank=True, to='backend_app.chat')),
                ('new_matches', models.ManyToManyField(blank=True, to='backend_app.game')),
            ],
        ),
    ]
