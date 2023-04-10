from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from users import serializers
from users.models import User
from users.services_user import UsersServices
from users.services_auth import AuthenticationServices


class RegistrationModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAdminUser(), ]
        return [AllowAny(), ]

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'register':
            return serializers.RegistrationSerializer
        elif hasattr(self, 'action') and self.action == 'login':
            return serializers.AuthenticationSerializer

        return serializers.UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hashed_password = make_password(serializer.validated_data.get('password'))
            serializer.save(password=hashed_password)
            return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = UsersServices.check_user(email, password)
            token = AuthenticationServices.encode_token(user)
            return Response(
                {
                    'username': user.username,
                    'token': token
                },
                status=status.HTTP_200_OK
            )
        except:
            res = {'error': 'Check you credentials'}
            return Response(res, status=status.HTTP_404_NOT_FOUND)
