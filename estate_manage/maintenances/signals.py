from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import WorkOrderLog, ServiceProvider, MaintenanceSchedule, WorkOrder


@receiver(post_save, sender=WorkOrder)
def log_work_order(sender, instance, created, **kwargs):
    if created:
        WorkOrderLog.objects.create(
            work_order=instance,
            status=instance.status,
            notes=instance.notes
        )
    else:
        log = WorkOrderLog.objects.filter(id=instance.id).last()
        log.status = instance.status
        log.notes = log.notes
        log.save()
