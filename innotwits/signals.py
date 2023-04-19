import json

from django.db.models import Count
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from innotwits.models import Post, Page
from innotwits.services import PostServices
from innotwits.tasks import send_email_task
from sender import send_to_fast_api


@receiver(post_save, sender=Post)
def send_email_after_post_signal(sender, instance, created, **kwargs):
    if created:
        post_id = instance.id
        title, text, emails = PostServices.create_mail(instance, post_id)
        send_email_task.delay(title, text, emails)


@receiver(post_save, sender=Page)
def new_page_created(sender, instance, created, **kwargs):
    if created:
        body = {'user_id': instance.owner.id,
                'page_id': instance.id,
                'posts_count': 0,
                'followers_count': 0,
                'likes_count': 0}
        send_to_fast_api(json.dumps(body))


@receiver(post_save, sender=Post)
def new_post_created(sender, instance, created, **kwargs):
    page = Page.objects.get(id=instance.page.id)
    posts = page.posts.count()

    body = {'user_id': instance.page.owner.id,
            'page_id': instance.page.id,
            'posts_count': posts,
            }
    send_to_fast_api(json.dumps(body))


@receiver(m2m_changed, sender=Post.like.through)
def update_page_likes(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        page = instance.page

        total_likes = page.posts.all().aggregate(total_likes=Count('likes'))['total_likes']
        body = {'user_id': instance.page.owner.id,
                'page_id': instance.page.id,
                'likes_count': total_likes,
                }
        send_to_fast_api(json.dumps(body))


@receiver(m2m_changed, sender=Page.followers.through)
def update_page_followers(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        total_followers = instance.followers.count()

        body = {'user_id': instance.owner.id,
                'page_id': instance.id,
                'followers_count': total_followers,
                }
        send_to_fast_api(json.dumps(body))
