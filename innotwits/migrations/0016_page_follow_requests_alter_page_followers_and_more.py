# Generated by Django 4.1.7 on 2023-03-21 12:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('innotwits', '0015_remove_page_follow_requests_alter_page_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='follow_requests',
            field=models.ManyToManyField(related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FollowerRequest',
        ),
    ]