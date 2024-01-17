from django.contrib import admin
from .models import Setting
from .models import ChatSession
from .models import Chat

admin.site.register(Setting)
admin.site.register(ChatSession)
admin.site.register(Chat)