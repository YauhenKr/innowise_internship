from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_image_file_extension
from django.db import models


def user_directory_path(instance, filename):
    return "images/user/{0}/{1}".format(instance.username, filename)


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_directory_path,
        validators=[validate_image_file_extension]
    )
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    created = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
