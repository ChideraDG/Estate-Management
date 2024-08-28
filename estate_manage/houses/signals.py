from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import House
from building_owners.models import BuildingOwner


@receiver(post_save, sender=House)
def building_owner(sender, instance, created, **kwargs):
    """
    Updates the building owner's portfolio size when a new House is created.
    
    If a new `House` instance is created and associated with a `BuildingOwner`, 
    this function increments the `portfolio_size` field of the `BuildingOwner`.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (House).
    instance : Model instance
        The instance of the model that was saved.
    created : bool
        A boolean indicating whether a new instance was created.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """
    if created and instance.building_owner:
        bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
        bo_user.portfolio_size += 1
        bo_user.save()


@receiver(pre_delete, sender=House)
def delete_building_owner(sender, instance, **kwargs):
    """
    Updates the building owner's portfolio size and deletes associated apartments 
    when a House is deleted.

    This function decrements the `portfolio_size` field of the associated `BuildingOwner` 
    and deletes all apartments associated with the `House` before the `House` instance 
    is deleted.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (House).
    instance : Model instance
        The instance of the model that is about to be deleted.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """
    if instance.building_owner:
        bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
        bo_user.portfolio_size -= 1
        bo_user.save()
    
    instance.apartments.all().delete()


@receiver(pre_save, sender=House)
def store_old_values(sender, instance, **kwargs):
    """
    Stores the old agent value before saving changes to a House instance.
    
    This function stores the current `agent` of a `House` instance as `old_agent` 
    before any updates to the `House` are saved. This is used to track changes 
    to the `agent` field.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (House).
    instance : Model instance
        The instance of the model that is about to be saved.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """
    if instance.pk:  # Only for existing instances
        old_instance = sender.objects.get(pk=instance.pk)
        instance.old_agent = old_instance.agent


@receiver(post_save, sender=House)
def house_agent(sender, instance, created, **kwargs):
    """
    Updates the agent's data when a new House is created or modified.
    
    When a new `House` is created or an existing `House` is updated, 
    this function handles the assignment and management of the associated 
    `Agent`, including updating the `date_of_hire` and `number_of_apartments_managed` fields.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (House).
    instance : Model instance
        The instance of the model that was saved.
    created : bool
        A boolean indicating whether a new instance was created.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """
    if created:
        if instance.number_of_apartments > 0 and instance.agent:
            agent = instance.agent
            agent.date_of_hire = instance.created
            agent.number_of_apartments_managed += instance.number_of_apartments
            agent.save()
        elif instance.agent:
            agent = instance.agent
            agent.date_of_hire = instance.created
            agent.save()
    else:
        if instance.old_agent is None and instance.agent:
            agent = instance.agent
            agent.date_of_hire = instance.created
            agent.number_of_apartments_managed += instance.number_of_apartments
            agent.save()
        elif instance.old_agent and instance.old_agent != instance.agent:
            instance.old_agent.number_of_apartments_managed -= instance.number_of_apartments
            instance.old_agent.save()

            agent = instance.agent
            agent.date_of_hire = instance.created
            agent.number_of_apartments_managed += instance.number_of_apartments
            agent.save()


@receiver(pre_delete, sender=House)
def house_agent_on_delete(sender, instance, **kwargs):
    """
    Updates the agent's data when a House is deleted.
    
    This function decrements the `number_of_apartments_managed` field for the 
    `Agent` associated with the `House` before the `House` instance is deleted.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (House).
    instance : Model instance
        The instance of the model that is about to be deleted.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """
    if instance.agent:
        agent = instance.agent
        agent.number_of_apartments_managed -= instance.number_of_apartments
        agent.save()
