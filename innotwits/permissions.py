from rest_framework import permissions

from users.models import User


class IsOwnerAdminModeratorCanEdit(permissions.BasePermission):
    """
    """
    allowed_fields = {'name', 'description', 'image', 'is_private'}
    admin_fields = {'is_blocked', 'unblock_date'}

    def has_object_permission(self, request, view, obj):
        role = request.user.role
        user = request.user
        owner = obj.owner

        if role in [User.Roles.ADMIN, User.Roles.MODERATOR] and request.method in ['PUT', 'PATCH']:
            fields = set(request.data.keys())
            if fields.issubset(self.admin_fields):
                return True

        elif role == User.Roles.USER and user == owner and request.method in ['PUT', 'PATCH']:
            fields = set(request.data.keys())
            if fields.issubset(self.allowed_fields):
                return obj.owner == request.user


class IsAdminModeratorDeleteIsOwnerDeleteUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        user = request.user
        page_user = obj.page.owner

        #  all([])
        if role in [User.Roles.USER, User.Roles.ADMIN, User.Roles.MODERATOR]\
                and request.method in ['PUT', 'PATCH', 'DELETE']\
                and user == page_user:
            return True

        elif role in [User.Roles.ADMIN, User.Roles.MODERATOR] and request.method in ['DELETE']:
            return True
