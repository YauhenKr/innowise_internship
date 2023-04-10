from rest_framework import serializers

from innotwits.models import Page, Post, Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class PageSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    tags = TagSerializer()
    post = serializers.SerializerMethodField(method_name='get_posts')

    class Meta:
        model = Page
        fields = ['name', 'description', 'owner', 'post', 'tags', 'is_private', ]

    def get_posts(self, obj):
        return PostSerializer(obj.posts, many=True).data


class PrivatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['name', ]


class CreatePageSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Page
        fields = ['name', 'description', 'owner', 'is_private']


class UpdatePageSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=False)

    class Meta:
        model = Page
        fields = ['name', 'description', 'owner', 'is_private', 'is_blocked']

        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'owner': {'required': False},
            'is_private': {'required': False},
            'is_blocked': {'required': False}
            # tag
        }


class ReplyToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    reply_to = ReplyToSerializer()

    class Meta:
        model = Post
        fields = ['page', 'content', 'created_at', 'reply_to']

        extra_kwargs = {
            'like': {'required': False},
            'reply_to': {'required': False},
        }
