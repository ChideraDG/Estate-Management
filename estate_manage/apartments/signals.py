from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import Apartment


@receiver(post_save, sender=Apartment)
def increase_number_of_apartments(sender, instance, created, **kwargs):
    """
    Increases the number of apartments in the associated house and updates occupancy status.

    This function listens to the `post_save` signal for the `Apartment` model. When a new `Apartment` 
    is created, it increments the `number_of_apartments` field in the associated `House`. 
    If the `Apartment` is occupied, the occupancy status of the `House` is updated to 'occupied'. 
    Additionally, if the `House` has an associated `Agent`, the `Agent`'s `number_of_apartments_managed` 
    field is incremented as well.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (Apartment).
    instance : Model instance
        The instance of the model that was saved.
    created : bool
        A boolean indicating whether a new instance was created (True) or an existing instance was updated (False).
    **kwargs : dict
        Additional keyword arguments passed by the signal.

    Notes
    -----
    - This function only increments the `number_of_apartments` field when a new `Apartment` is created.
    - If an existing `Apartment` is updated, the function only checks for occupancy status changes.
    """
    house = instance.house
    if created:
        if instance.is_occupied:
            house.occupancy_status = 'occupied'
        house.number_of_apartments += 1
        house.save()

        if house.agent:
            agent = house.agent
            agent.number_of_apartments_managed += 1
            agent.save()
    else:
        if instance.is_occupied:
            house.occupancy_status = 'occupied'
        house.save()


@receiver(pre_delete, sender=Apartment)
def decrease_number_of_apartments(sender, instance, **kwargs):
    """
    Decreases the number of apartments in the associated house and updates occupancy status.

    This function listens to the `pre_delete` signal for the `Apartment` model. Before an `Apartment` 
    is deleted, it decrements the `number_of_apartments` field in the associated `House`. 
    If the `House` only has one `Apartment` remaining, the occupancy status is updated to 'vacant'. 
    Additionally, if the `House` has an associated `Agent`, the `Agent`'s `number_of_apartments_managed` 
    field is decremented.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (Apartment).
    instance : Model instance
        The instance of the model that is about to be deleted.
    **kwargs : dict
        Additional keyword arguments passed by the signal.

    Notes
    -----
    - This function ensures that the `House` occupancy status is set to 'vacant' if the last `Apartment` is deleted.
    """
    house = instance.house
    if house.number_of_apartments == 1:
        house.occupancy_status = 'vacant'
    
    house.number_of_apartments -= 1
    house.save()

    if house.agent:
        agent = house.agent
        agent.number_of_apartments_managed -= 1
        agent.save()
