from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import *


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
            designation=user.last_name,
        )

        subject = 'Welcome to EstateManage'
        recipient = [user.email]
        message = f"""Dear {user.username},

Welcome to EstateManage!

We’re delighted to have you as a new client. At EstateManage, we specialize in comprehensive estate management solutions tailored to meet your needs. Our team is committed to providing exceptional service and ensuring your properties are managed efficiently.

Should you have any questions or require assistance, please don’t hesitate to reach out. We’re here to support you every step of the way.

Thank you for choosing EstateManage. We look forward to a successful partnership!

Best regards,
The EstateManage Team"""

        send_mail(subject=subject,
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=recipient,
                  fail_silently=False)
