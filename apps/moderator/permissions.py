from rest_framework.permissions import BasePermission

class ModeratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class ModeratorObjectPermission(BasePermission):
    def has_object_permission(self, request, obj, view):
        return request.user.is_superuser