from innotwits.models import Page


def create_user_page_signal(sender, instance, created, *args, **kwargs):
    if not instance.created:
        Page.objects.create(owner=instance)
        instance.created = True
        instance.save()
