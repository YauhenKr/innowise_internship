# Generated by Django 4.1.7 on 2023-03-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.BooleanField(default=False),
        ),
    ]