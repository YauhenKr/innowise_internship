from innotwits.models import Page


def block_unblock_signal(sender, instance, created, **kwargs):
    Page.objects.filter(owner=instance.pk).update(is_blocked=instance.is_blocked)
