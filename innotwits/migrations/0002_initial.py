# Generated by Django 4.1.7 on 2023-03-10 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('innotwits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='follow_requests',
            field=models.ManyToManyField(related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(related_name='pages', to='innotwits.tag'),
        ),
    ]
