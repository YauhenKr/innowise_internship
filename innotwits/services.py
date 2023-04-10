import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from innotwits.models import Page, Tag, Post
from innotwits import serializers
from users.models import User


class PageServices:
    @classmethod
    def get_page_by_access(cls, user_role, staff_or_not, page_id, user) -> serializers:
        page = get_object_or_404(Page, pk=page_id)

        if user_role == 'admin' or user_role == 'moderator' or staff_or_not or\
                (user_role == 'user' and page.is_private is False
                 and page.owner.is_blocked is False) or page.owner == user:
            return serializers.PageSerializer(
                page,
                many=False
            ).data

        elif user_role == 'user' and page.owner.is_blocked is False:
            if page.is_private:
                return serializers.PrivatePageSerializer(
                    page,
                    many=False
                ).data

        else:
            raise exceptions.NotAcceptable

    @classmethod
    def create_page(cls, name, description, user, is_private=False) -> Page:
        return Page.objects.create(
            name=name,
            description=description,
            owner_id=user.pk,
            is_private=is_private
        )

    @classmethod
    def create_delete_tag(cls, method, tag, page) -> str:
        if method == 'POST':
            tag, created = Tag.objects.get_or_create(name=tag)
            if not created:
                return 'Tag is already exists'
            page.tags.add(tag)

        elif method == 'DELETE':
            try:
                tag_to_delete = page.tags.get(name__exact=tag)
            except Tag.DoesNotExist:
                raise Http404
            page.tags.remove(tag_to_delete)
            return 'Tag was deleted'
        return 'Tag was successfully added'

    @classmethod
    def subscribe_to_page(cls, user_id, page_id) -> [bool, str]:
        try:
            user = User.objects.get(id=user_id)
            page = Page.objects.get(id=page_id)

            if page.followers.filter(id=user_id).exists():
                return False, 'Your subscription request has already been sent'

            if page.owner == user:
                return False, 'You cannot subscribe to yourself'

            if page.is_private:

                page.follow_requests.add(user)
                return True, 'Follow request has been sent'
            else:

                page.followers.add(user)
                return True, 'You have subscribed to the page'

        except ObjectDoesNotExist:
            return False, 'User/page does not exist'

    @classmethod
    def unfollow_page(cls, user_id, page, unfollow) -> [bool, str]:
        User.objects.get(id=user_id)
        try:
            if unfollow and page.followers.filter(id=user_id).exists():
                page.followers.remove(user_id)
                return True, 'You have just unfollowed that user'

            else:
                return False, 'You are not friends'

        except ObjectDoesNotExist:
            return False, 'You are not friends'

    @classmethod
    def approve_disapprove_request(cls, page, user, request_user_ids, accept) -> str:
        if page.owner == user:
            if accept:
                for user_id in page.follow_requests.filter(id__in=request_user_ids):
                    page.followers.add(user_id)
                    page.follow_requests.remove(user_id)
                return "User's requests were approved successfully"

            else:
                for user_id in page.follow_requests.filter(id__in=request_user_ids):
                    page.follow_requests.remove(user_id)
                return 'All requests were disapproved successfully'

        else:
            return 'Forbidden. It is not your page!'

    @classmethod
    def get_requests_list(cls, user_id, page_id):
        try:
            user = User.objects.get(id=user_id)
            page = Page.objects.get(id=page_id)

            if page.owner == user:
                return page.follow_requests.all(),

        except ObjectDoesNotExist:
            return False, 'You have no one request'

    @classmethod
    def unblock_page(cls) -> None:
        now = datetime.datetime.today().strftime('%Y-%m-%d')
        Page.objects.filter(unblock_date__contains=now).update(is_blocked=False)
        return None


class PostServices:
    @classmethod
    def get_page_id(cls, page, request) -> [str or bool]:
        page_id = page.pk
        page_ids = Page.objects.filter(owner=request.user.pk).values_list('id', flat=True)
        if page_id not in page_ids:
            return False

        return page_id

    @classmethod
    def get_liked_posts(cls, posts, request) -> list:
        liked_posts = []
        for post in posts:
            if post.like.filter(id=request.user.pk).exists():
                liked_posts.append(post)

        return liked_posts

    @classmethod
    def get_posts_list(cls, user, posts) -> Post:
        followed_pages_id = Page.objects.filter(followers=user.pk).values_list('id', flat=True)
        posts = posts.filter(Q(page__owner=user.pk) | Q(page__in=followed_pages_id)).\
            filter(reply_to__isnull=True).order_by('created_at')

        return posts

    @classmethod
    def create_new_post(cls, page_id, serializer, reply_to) -> Post:
        create_post = Post.objects.create(
            page_id=page_id,
            content=serializer.validated_data.get('content'),
            reply_to=reply_to
        )

        return create_post

    @classmethod
    def create_mail(cls, instance, post_id):
        title = f'New post from page {instance}'
        text = f'This is proof the task worked! http://127.0.0.1:8000/post/{post_id}/ link to post'
        emails = instance.page.followers.all().values_list('email', flat=True)

        return title, text, list(emails)
