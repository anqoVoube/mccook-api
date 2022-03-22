from django.contrib import admin
from apps.client.models.client import Client, User


admin.site.register(User)
admin.site.register(Client)