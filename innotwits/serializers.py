from rest_framework import serializers

from innotwits.models import Page, Post, Tag
from users.serializers import UserSerializer


class PageSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    post = serializers.SerializerMethodField(method_name='get_posts')

    class Meta:
        model = Page
        fields = ['name', 'description', 'owner', 'post', 'is_private', ]           # add image

    def get_posts(self, obj):
        return PostSerializer(obj.posts, many=True).data


class PrivatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['name', ]           # add image


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    # page = PageSerializer() I can't work through this serializers because 'This field is required'

    class Meta:
        model = Post
        fields = ['page', 'content']

        extra_kwargs = {
            'like': {'required': False},
        }


# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['page']

