import jwt
from django.conf import settings
from django.http import JsonResponse

from users.services_auth import AuthenticationServices
from users.services_user import UsersServices


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            header = request.headers.get('authorization')
            if header:
                token = AuthenticationServices.get_the_token_from_header(header)
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    user = UsersServices.get_user_through_payload(payload)
                    if not user:
                        return JsonResponse({'error': 'User not found.'}, status=401)
                    request.user = user
                except jwt.DecodeError:
                    return JsonResponse({'error': 'Invalid token.'}, status=401)
        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'DRF_error': 'Token has expired'}, status=401)

        response = self.get_response(request)
        return response
