class ReadAllEditAdmin(permissions.BasePermission):
    message = _("You must be superuser to edit.")

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or request.user.is_superuser


class ReadOwnEditOwn(permissions.BasePermission):
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

