from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем запись только автору
        return obj.author == request.user
