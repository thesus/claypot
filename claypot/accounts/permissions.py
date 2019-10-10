from rest_framework import permissions

from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _


class ReadSelf(permissions.BasePermission):
    message = _("You may only view your own profile.")

    def has_permission(self, request, view):
        if view.action_map.get(request.method.lower(), None) == "retrieve":
            return request.user.is_authenticated or request.user.is_superuser
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if view.action_map.get(request.method.lower(), None) == "retrieve":
            if request.method in permissions.SAFE_METHODS:
                if isinstance(obj, get_user_model()):
                    return obj == request.user
        return request.user.is_superuser
