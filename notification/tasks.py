from celery import Celery, shared_task
from InventorySystem import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from unreturned.models import Unreturned_Item
from recents.models import Borrowed_Item
from django.contrib.auth.models import User  # Import User model

app = Celery('notification', broker='redis://127.0.0.1:6379')

@shared_task(bind=True)
def send_mail_func(self):
    # Get users with unreturned items
    users_with_unreturned_items = User.objects.filter(
        borrowed_item__item_returned=False
    ).distinct()

    for user in users_with_unreturned_items:
        mail_subject = "Unreturned Items Reminder"
        message = "You have unreturned items. Please return them as soon as possible. For more information please check the unreturned tab!\n\nThank you for your understanding."
        to_email = user.email

        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )

    return "Task Successful"

