from django.db import models


# ChatSession logged represents a collection of chats under a given name.
class ChatSession(models.Model):
    session_id = models.UUIDField(primary_key=True)
    session_name = models.CharField(max_length=200)
    chats = models.ManyToManyField("Chat")

    def __str__(self):
        return self.session_name


# Chat contains logged individual requests and responses.
class Chat(models.Model):
    chat_id = models.UUIDField(primary_key=True)
    chat_text = models.TextField()
    response_text = models.TextField()
    timestamp_chat = models.DateTimeField("date chat sent")
    timestamp_response = models.DateTimeField("date response received")

    def __str__(self):
        return self.chat_text


# Setting contains configuration settings for the interface.
class Setting(models.Model):
    setting_id = models.UUIDField(primary_key=True)
    setting_name = models.CharField(max_length=200)
    setting_value = models.CharField(max_length=200)

    def __str__(self):
        return self.setting_name
