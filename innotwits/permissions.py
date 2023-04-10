from rest_framework import permissions

from users.models import User


class IsOwnerAdminModeratorCanEdit(permissions.BasePermission):
    allowed_fields = {'name', 'description', 'image', 'is_private'}
    admin_fields = {'is_blocked', 'unblock_date'}

    def has_object_permission(self, request, view, obj):
        role, user, owner = request.user.role, request.user, obj.owner

        if role in [User.Roles.ADMIN, User.Roles.MODERATOR] and request.method in ['PUT', 'PATCH']:
            fields = set(request.data.keys())
            if fields.issubset(self.admin_fields):
                return True

        elif all([
            role == User.Roles.USER,
            user == owner,
            request.method in ['PUT', 'PATCH']
        ]):
            fields = set(request.data.keys())
            if fields.issubset(self.allowed_fields):
                return obj.owner == request.user


class IsAdminModeratorDeleteIsOwnerDeleteUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        role, user, page_user = request.user.role, request.user, obj.page.owner

        if all([
            role in [User.Roles.USER, User.Roles.ADMIN, User.Roles.MODERATOR],
            request.method in ['PUT', 'PATCH', 'DELETE'],
            user == page_user
        ]):
            return True

        elif role in [User.Roles.ADMIN, User.Roles.MODERATOR] and request.method in ['DELETE']:
            return True
