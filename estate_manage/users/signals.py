from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile


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


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

    subject = 'Confirmation of Profile Deletion from EstateManage'
    recipient = [user.email]
    message = f"""
Dear {instance.name},

We hope this message finds you well. This is to confirm that your profile has been successfully deleted from EstateManage as per your request.

We’re sorry to see you go and would like to extend our heartfelt thanks for being a part of our community. Your engagement has been invaluable, and we truly appreciate the trust you placed in us for your estate management needs.

Should you decide to rejoin us in the future or if you have any questions or need further assistance, please don’t hesitate to reach out. We’re always here to help.

Thank you once again for choosing EstateManage. We wish you all the best in your future endeavors.

Best regards,
The EstateManage Team
Phone Number: +234 7033327493"""
    
    send_mail(subject=subject,
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=recipient,
                  fail_silently=False)
