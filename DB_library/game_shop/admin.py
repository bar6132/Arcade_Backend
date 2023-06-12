from django.contrib import admin
from .models import UserProfile, Game, ContactMsg, Message

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(ContactMsg)
admin.site.register(Message)
