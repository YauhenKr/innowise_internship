from __future__ import absolute_import, unicode_literals
import os

from celery import shared_task
from django.core.mail import send_mail

from innotwits.services import PageServices


@shared_task
def send_email_task(title, text, emails):
    send_mail(
        title,
        text,
        os.getenv('EMAIL_FROM'),
        emails
    )

    return "Sending was successfully finished"


@shared_task
def unblock_page():
    PageServices.unblock_page()
    return "Page unblocking"
