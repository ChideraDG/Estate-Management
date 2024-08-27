from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import House
from building_owners.models import BuildingOwner
from agents.models import Agent


@receiver(post_save, sender=House)
def all_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.building_owner:
            bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
            bo_user.portfolio_size += 1
            bo_user.save()
        
        if instance.agent:
            agent = Agent.objects.get(id=instance.agent.id)
            agent.date_of_hire = instance.created
            agent.number_of_apartments_managed += instance.number_of_apartments
            agent.save()
    else:
        if instance.agent:
            agent = Agent.objects.get(id=instance.agent.id)
            agent.date_of_hire = instance.updated
            agent.number_of_apartments_managed += instance.number_of_apartments
            agent.save()


@receiver(pre_delete, sender=House)
def all_pre_delete(sender, instance, **kwargs):
    if instance.building_owner:
        bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
        bo_user.portfolio_size -= 1
        bo_user.save()
    
    instance.apartments.all().delete()

    if instance.agent:
            agent = Agent.objects.get(id=instance.agent.id)
            agent.number_of_apartments_managed -= instance.number_of_apartments
            agent.save()
