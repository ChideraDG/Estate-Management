from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile
from .models import Tenant


@receiver(post_save, sender=Profile)
def createBuyerProfile(sender, instance, created, **kwargs):
    """
    Creates a new Tenant profile when a new Profile instance is saved with 'tenant' designation.

    Args:
        sender (type): The model that sent the signal.
        instance (Profile): The instance of the Profile model that was saved.
        created (bool): Whether a new instance was created.

    Example:
        When a new Profile instance is created with 'tenant' designation, a new Tenant instance will be created automatically.

        >>> from users.models import Profile
        >>> profile = Profile.objects.create(name='Example Tenant', email='example@example.com', designation='tenant')
        >>> Tenant.objects.get(user=profile)
        <Tenant: Example Tenant>

    """
    if created:
        user = instance
        if user.designation == 'tenant':
            Tenant.objects.create(
                user=user,
                first_name=user.name,
                email=user.email,
            )