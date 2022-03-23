from rest_framework.permissions import BasePermission
from apps.client.models.client import Client


class RateRecipe(BasePermission):
    def has_object_permission(self, request, view, obj):
        client_user = Client.objects.get(client_user=request.user)
        return obj.by_cook != client_user

class RateClient(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.client_user != request.user
