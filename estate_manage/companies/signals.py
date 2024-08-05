from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile
from .models import Company


@receiver(post_save, sender=Profile)
def createCompanyProfile(sender, instance, created, **kwargs):
    """
    Creates a new Company profile when a new Profile instance is saved with 'company' designation.

    Args:
        sender (type): The model that sent the signal.
        instance (Profile): The instance of the Profile model that was saved.
        created (bool): Whether a new instance was created.

    Example:
        When a new Profile instance is created with 'company' designation, a new Company instance will be created automatically.

        >>> from users.models import Profile
        >>> profile = Profile.objects.create(name='Example Company', email='example@example.com', designation='company')
        >>> Company.objects.get(owner=profile)
        <Company: Example Company>

    """
    if created:
        user = instance
        if user.designation == 'company':
            Company.objects.create(
                owner=user,
                name=user.name,
                email=user.email,
            )