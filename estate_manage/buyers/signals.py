from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile
from .models import Buyer


@receiver(post_save, sender=Profile)
def createBuyerProfile(sender, instance, created, **kwargs):
    """
    Creates a new Buyer profile when a new Profile instance is saved with 'buyer' designation.

    Args:
        sender (type): The model that sent the signal.
        instance (Profile): The instance of the Profile model that was saved.
        created (bool): Whether a new instance was created.

    Example:
        When a new Profile instance is created with 'buyer' designation, a new Buyer instance will be created automatically.

        >>> from users.models import Profile
        >>> profile = Profile.objects.create(name='Example Buyer', email='example@example.com', designation='buyer')
        >>> Buyer.objects.get(user=profile)
        <Buyer: Example Buyer>

    """
    if created:
        user = instance
        if user.designation == 'buyer':
            Buyer.objects.create(
                user=user,
                full_name=user.name,
                email=user.email,
            )