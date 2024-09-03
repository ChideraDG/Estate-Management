from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile
from .models import BuildingOwner
from tenants.models import Tenant


@receiver(post_save, sender=Profile)
def create_building_owner_profile(sender, instance, created, **kwargs):
    """
    Creates a new Building Owner profile when a new Profile instance is saved with 'Building Owner' designation.

    Args:
        sender (type): The model that sent the signal.
        instance (Profile): The instance of the Profile model that was saved.
        created (bool): Whether a new instance was created.

    Example:
        When a new Profile instance is created with 'bilding_owner' designation, a new Building Owner instance will be created automatically.

        >>> from users.models import Profile
        >>> profile = Profile.objects.create(name='Example Building Owner', email='example@example.com', designation='building_owner')
        >>> BuildingOwne.objects.get(user=profile)
        <Building Owner: Example Building Owner>

    """
    if created:
        user = instance
        if user.designation == 'building_owner':
            BuildingOwner.objects.create(
                user=user,
                building_owner_name=user.name,
                contact_email=user.email,
            )
            