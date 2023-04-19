from django.db.models.signals import post_save
from django.dispatch import receiver

from innotwits.models import Page
from users.models import User


@receiver(post_save, sender=User)
def block_unblock_signal(sender, instance, created, **kwargs):
    if instance.is_blocked:
        Page.objects.filter(owner=instance.pk).update(is_blocked=True)
    elif not instance.is_blocked:
        Page.objects.filter(owner=instance.pk).update(is_blocked=False)
