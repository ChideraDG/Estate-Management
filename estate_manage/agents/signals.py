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
    """
    Disconnects the Agent from associated Houses before deleting the Agent.

    This function listens to the `pre_delete` signal for the `Agent` model. 
    Before an `Agent` instance is deleted, it loops through all associated `House` instances 
    and sets their `agent` field to `None`, effectively removing the association with the agent.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (Agent).
    instance : Model instance
        The instance of the model that is about to be deleted.
    **kwargs : dict
        Additional keyword arguments passed by the signal.

    Notes
    -----
    This function should be connected to the `pre_delete` signal in the Django app's ready function 
    or directly within the model's signals setup to ensure that it operates correctly.

    Example
    -------
    If an `Agent` with associated `Houses` is deleted, this function will ensure that
    the `agent` field for each `House` is set to `None` before the `Agent` instance is deleted.
    """
    houses = instance.houses.all()
    for house in houses:
        house.agent = None
        house.save()
    