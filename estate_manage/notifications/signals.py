from django.db.models.signals import post_save
from django.dispatch import receiver
from maintenances.models import WorkOrder
from .models import Notification


@receiver(post_save, sender=WorkOrder)
def log_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            title=f"{instance.apartment.tenant_apartment.user.name} sent a Work order Request",
            message=instance.description,
            user=instance.apartment.tenant_apartment.building_owner.user.user if instance.apartment.tenant_apartment.building_owner else instance.apartment.tenant_apartment.company.user.user,
            notification_type = "MU"
        )
