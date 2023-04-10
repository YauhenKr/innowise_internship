import datetime
import jwt
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password

from core.settings import JWT_AUTH
from users.models import User


def encode_token(user: User) -> str:
    payload = {
        'user_id': user.pk,
        'username': user.username,
        'exp': (datetime.datetime.now() + JWT_AUTH.get('JWT_EXPIRATION_DELTA')).timestamp()
    }

    token = jwt.encode(
        payload=payload,
        key=JWT_AUTH.get('SIGNING_KEY'),
        algorithm=JWT_AUTH.get('ALGORITHM')
    )

    return token


def get_the_token_from_header(token) -> str:
    token = token.replace('Bearer ', '').replace(' ', '')
    return token


def get_user_by_email(email) -> User:
    user = get_object_or_404(User, email=email)
    return user


def _get_user_through_payload(payload) -> User:
    return User.objects.filter(id=payload['user_id']).first()


def check_user(email, password) -> User:
    user = get_user_by_email(email)
    user = get_object_or_404(User, username=user.username)

    if not check_password(password, user.password):
        raise AuthenticationFailed('Invalid password.')

    return user


def create_details(user, token) -> dict:
    return {'username': user.username, 'token': token}






