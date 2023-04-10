from django.db.models.signals import post_save
from django.dispatch import receiver

from innotwits.models import Post
from innotwits.services import PostServices
from innotwits.tasks import send_email_task


@receiver(post_save, sender=Post)
def send_email_after_post_signal(sender, instance, created, **kwargs):
    if created:
        post_id = instance.id
        title, text, emails = PostServices.create_mail(instance, post_id)
        send_email_task.delay(title, text, emails)
