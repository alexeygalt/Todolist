from django.contrib import admin

# Register your models here.
from bot.models import TgUser

admin.site.register(TgUser)
