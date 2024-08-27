from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import Profile
from .models import Agent


@receiver(post_save, sender=Profile)
def createAgentProfile(sender, instance, created, **kwargs):
    """
    Creates a new Agent profile when a new Profile instance is saved with 'agent' designation.

    Args:
        sender (type): The model that sent the signal.
        instance (Profile): The instance of the Profile model that was saved.
        created (bool): Whether a new instance was created.

    Example:
        When a new Profile instance is created with 'agent' designation, a new Agent instance will be created automatically.

        >>> from users.models import Profile
        >>> profile = Profile.objects.create(name='Example Agent', email='example@example.com', designation='agent')
        >>> Agent.objects.get(user=profile)
        <Agent: Example Agent>

    """
    if created:
        user = instance
        if user.designation == 'agent':
            Agent.objects.create(
                user=user,
                name=user.name,
                email=user.email,
            )


@receiver(pre_delete, sender=Agent)
def deleteAgentProfile(sender, instance, **kwargs):
    houses = instance.houses.all()
    for house in houses:
        house.agent = None
        house.save()
    