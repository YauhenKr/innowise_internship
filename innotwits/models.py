import uuid
from datetime import datetime

from django.core.validators import validate_image_file_extension
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.name)

    objects = models.Manager()


def user_directory_path(instance, filename):
    page_name = instance.name
    current_date = datetime.now().strftime('%Y-%m-%d')
    return f"pages/{page_name}/{current_date}/{filename}"


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='pages')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', related_name='follows')

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_directory_path,
        validators=[validate_image_file_extension]
    )

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User', related_name='requests')

    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner.username} | {self.name}"

    objects = models.Manager()


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField('users.User', related_name='likes')

    reply_to = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True, related_name='replies')

    def __str__(self):
        return str(f'{self.page.owner.username} | {self.content}')

    objects = models.Manager()
