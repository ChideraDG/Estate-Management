from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import Profile
from building_owners.models import BuildingOwner
from agents.models import Agent
from tenants.models import Tenant


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Creates a new Profile instance when a new User instance is created.

    Args:
        sender (type): The model that sent the signal.
        instance (User): The User instance that was created.
        created (bool): Whether the User instance was created or updated.

    Example:
        When a new User instance is created, this function will be called automatically.
        It will create a new Profile instance with the same username, email, and name as the User instance.

        >>> from django.contrib.auth.models import User
        >>> user = User.objects.create_user('john', 'john@example.com', 'password')
        >>> profile = Profile.objects.get(user=user)
        >>> profile.username
        'john'
        >>> profile.email
        'john@example.com'
        >>> profile.name
        'John'
    """
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
def delete_user(sender, instance, **kwargs):
    """
    Deletes the associated User instance when a Profile instance is deleted.

    Args:
        sender (type): The model that sent the signal.
        instance (Profile): The Profile instance that was deleted.

    Example:
        When a Profile instance is deleted, this function will be called automatically.
        It will delete the associated User instance.

        >>> from .models import Profile
        >>> profile = Profile.objects.get(id=1)
        >>> profile.delete()
        >>> User.objects.filter(id=profile.user.id).exists()
        False
    """
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
    

@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        if " " in instance.name:
            instance.user.first_name = instance.name.split(" ")[0]
            instance.user.last_name = instance.name.split(" ")[1]
        else:
            instance.user.first_name = instance.name
        instance.user.username = instance.username
        instance.user.email = instance.email

        if instance.designation == 'building_owner':
            bo = BuildingOwner.objects.filter(user=instance).first()
            if bo:
                bo.building_owner_name = instance.name
                bo.contact_email = instance.email
                bo.contact_phone = instance.phone_number
                bo.profile_pics = instance.profile_image
                bo.save()

        if instance.designation == 'agent':
            agent = Agent.objects.filter(user=instance).first()
            if agent:
                agent.name = instance.name
                agent.email = instance.email
                agent.phone_number = instance.phone_number
                agent.profile_picture = instance.profile_image
                agent.save()
        
        if instance.designation == 'tenant':
            tenant = Tenant.objects.filter(user=instance).first()
            if tenant:
                if " " in instance.name:
                    tenant.first_name = instance.name.split(" ")[0]
                    tenant.last_name = instance.name.split(" ")[1]
                else:
                    tenant.first_name = instance.name
                tenant.email = instance.email
                tenant.phone_number = instance.phone_number
                tenant.profile_picture = instance.profile_image
                tenant.save()
                
        instance.user.save()


@receiver(post_delete, sender=User)
def delete_user_sessions(sender, instance, **kwargs):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(instance.id):
            session.delete()