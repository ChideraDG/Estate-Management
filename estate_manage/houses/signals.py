from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import House
from building_owners.models import BuildingOwner


@receiver(post_save, sender=House)
def add_portfolio_size(sender, instance, created, **kwargs):
    if created:
        if instance.building_owner:
            bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
            bo_user.portfolio_size += 1
            bo_user.save()


@receiver(pre_delete, sender=House)
def delete_portfolio_size(sender, instance, **kwargs):
    if instance.building_owner:
        bo_user = BuildingOwner.objects.get(id=instance.building_owner.id)
        bo_user.portfolio_size -= 1
        bo_user.save()


@receiver(pre_delete, sender=House)
def delete_apartments(sender, instance, **kwargs):
    instance.apartments.all().delete()