# Generated by Django 4.1.7 on 2023-03-20 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innotwits', '0007_alter_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='likes', to='innotwits.page'),
        ),
    ]