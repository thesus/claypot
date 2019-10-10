from pytz import utc
from datetime import datetime

from rest_framework import permissions

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from claypot.models import RecipeDraft, Recipe


class ReadAllEditAdmin(permissions.BasePermission):
    """Allows read acccess to all and restrict write access to admin users."""

    message = _("You must be superuser to edit.")

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or request.user.is_superuser
            or request.user.is_staff
        )


class ReadOwnEditOwn(permissions.BasePermission):
    """Allows read access if the author of the object is the logged in user.

    Used for `claypot.models.RecipeDraft`.
    """

    message = _("You may only read an edit your own data.")

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        elif isinstance(obj, RecipeDraft):
            if obj.author == request.user:
                return True
        return False


class ReadAllEditOwn(permissions.BasePermission):
    """Allow read access to everyone and restrict edit to superuser and author.

    Restricts deleting of models to admins after a grace period
    specified in the settings. Used for `claypot.models.Recipe`.
    """

    message = _("You may only edit your own recipes.")

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or request.user.is_authenticated
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Recipe):
            if obj.author == request.user:
                if view.action != "destroy":
                    return True
                else:
                    now = datetime.utcnow().replace(tzinfo=utc)
                    cut_off = now - settings.RECIPE_DELETE_GRACE_PERIOD
                    return obj.published_on > cut_off
        else:
            return False
