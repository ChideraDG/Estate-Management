from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import House
from building_owners.models import BuildingOwner
from agents.models import Agent


@receiver(post_save, sender=House)
def building_owner(sender, instance, created, **kwargs):
    if created:
        if instance.building_owner:
            bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
            bo_user.portfolio_size += 1
            bo_user.save()


@receiver(pre_delete, sender=House)
def delete_building_owner(sender, instance, **kwargs):
    if instance.building_owner:
        bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
        bo_user.portfolio_size -= 1
        bo_user.save()
    
    instance.apartments.all().delete()

@receiver(pre_save, sender=House)
def store_old_values(sender, instance, **kwargs):
    if instance.pk:  # Only do this for existing instances (not on creation)
        old_instance = sender.objects.get(pk=instance.pk)
        instance.old_agent = old_instance.agent

@receiver(post_save, sender=House)
def house_agent(sender, instance, created, **kwargs):
    if created:
        if instance.number_of_apartments > 0:
            if instance.agent:
                agent = instance.agent
                agent.date_of_hire = instance.created
                agent.number_of_apartments_managed += instance.number_of_apartments
                agent.save()
        else:
            if instance.agent:
                agent = instance.agent
                agent.date_of_hire = instance.created
                agent.save()
    else:
        if not (instance.old_agent is not None):
            agent = instance.agent
            agent.date_of_hire = instance.created
            agent.number_of_apartments_managed += instance.number_of_apartments
            agent.save()
        elif (instance.old_agent is not None) and instance.old_agent != instance.agent:
            instance.old_agent.number_of_apartments_managed -= instance.number_of_apartments
            instance.old_agent.save()

            instance.agent.date_of_hire = instance.created
            instance.agent.number_of_apartments_managed += instance.number_of_apartments
            instance.agent.save()

@receiver(pre_delete, sender=House)
def house_agent(sender, instance, **kwargs):
    if instance.agent:
        agent = instance.agent
        agent.number_of_apartments_managed -= instance.number_of_apartments
        agent.save()