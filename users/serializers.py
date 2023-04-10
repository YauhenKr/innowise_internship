from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_blocked']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', ]


class AuthenticationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', ]

        extra_kwargs = {
            'email': {'required': True, 'validators': []}, }
