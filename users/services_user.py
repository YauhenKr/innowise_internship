from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class UsersServices:
    @classmethod
    def get_user_by_email(cls, email) -> User:
        return User.objects.get(email=email)

    @classmethod
    def get_user_through_payload(cls, payload) -> User:
        return User.objects.filter(pk=payload['user_pk']).first()

    @classmethod
    def check_user(cls, email, password) -> User:
        user = cls.get_user_by_email(email)
        user = get_object_or_404(User, username=user.username)

        if not check_password(password, user.password):
            raise AuthenticationFailed('Invalid password.')

        return user
