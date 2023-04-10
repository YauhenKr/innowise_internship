import datetime
from typing import Any

import jwt
from rest_framework import exceptions

from core import settings
from users.models import User


class AuthenticationServices:
    @classmethod
    def encode_token(cls, user: User) -> str:
        payload = {
            'user_id': user.pk,
            'username': user.username,
            'exp': (datetime.datetime.now() + settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')).timestamp()
        }

        token = jwt.encode(
            payload=payload,
            key=settings.JWT_AUTH.get('SIGNING_KEY'),
            algorithm=settings.JWT_AUTH.get('ALGORITHM')
        )

        return token

    @classmethod
    def get_user_through_payload(cls, payload) -> User:
        return User.objects.filter(pk=payload['user_id']).first()

    @classmethod
    def get_the_token_from_header(cls, token) -> str:
        token = token.replace('Bearer ', '').replace(' ', '')
        return token

    @classmethod
    def check_jwt_token(cls, header) -> Any:
        jwt_token = AuthenticationServices.get_the_token_from_header(header)
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('Invalid signature')
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')

        return payload
