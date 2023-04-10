from innotwits.models import Page


def block_unblock_signal(sender, instance, created, **kwargs):
    if instance.is_blocked:
        Page.objects.filter(owner=instance.pk).update(is_blocked=True)
    elif not instance.is_blocked:
        Page.objects.filter(owner=instance.pk).update(is_blocked=False)
