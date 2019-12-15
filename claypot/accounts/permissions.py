from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions


class ReadSelf(permissions.BasePermission):
    """Permits access to the (user)model instance if the user corresponds to the instance"""

    message = _("You may only view your own profile.")

    def has_permission(self, request, view):
        if view.action_map.get(request.method.lower(), None) == "retrieve":
            return request.user.is_authenticated or request.user.is_superuser
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action_map.get(request.method.lower(), None) == "retrieve":
            if request.method in permissions.SAFE_METHODS:
                if isinstance(obj, get_user_model()) and obj == request.user:
                    return True
        return request.user.is_superuser
