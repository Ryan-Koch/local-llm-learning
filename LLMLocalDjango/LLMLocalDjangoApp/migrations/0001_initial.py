# Generated by Django 4.2.7 on 2023-11-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_id', models.UUIDField(primary_key=True, serialize=False)),
                ('chat_text', models.TextField()),
                ('response_text', models.TextField()),
                ('timestamp_chat', models.DateTimeField(verbose_name='date chat sent')),
                ('timestamp_response', models.DateTimeField(verbose_name='date response received')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('setting_id', models.UUIDField(primary_key=True, serialize=False)),
                ('setting_name', models.CharField(max_length=200)),
                ('setting_value', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('session_id', models.UUIDField(primary_key=True, serialize=False)),
                ('session_name', models.CharField(max_length=200)),
                ('chats', models.ManyToManyField(to='LLMLocalDjangoApp.chat')),
            ],
        ),
    ]
