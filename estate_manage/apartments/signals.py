from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import Apartment


@receiver(post_save, sender=Apartment)
def increase_number_of_apartments(sender, instance, created, **kwargs):
    house  = instance.house
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
    house  = instance.house
    if house.number_of_apartments == 1:
        house.occupancy_status = 'vacant'
        
    house.number_of_apartments -= 1
    house.save()

    if house.agent:
        agent = house.agent
        agent.number_of_apartments_managed -= 1
        agent.save()