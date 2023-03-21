from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from users.services_auth import AuthenticationServices
from users.services_user import UsersServices


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('authorization')
        if header:
            payload = AuthenticationServices.check_jwt_token(header)
            user = UsersServices.get_user_through_payload(payload)
            if user is None:
                raise AuthenticationFailed('User not found')

            return user, payload

        return None
