from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, pre_delete
from finances.models import RentPayment
from houses.models import House
from apartments.models import Apartment
from maintenances.models import WorkOrder
from .models import ActivityLog


@receiver(signal=user_logged_in)
def user_login(sender, request, user, **kwargs):
    ActivityLog.objects.create(
        user=user,
        action_type="Login",
        colour="success",
        description=f"{user.username} logged in",
    )
    # print(request.META.get('REMOTE_ADDR'))

@receiver(signal=user_logged_out)
def user_logout(sender, request, user, **kwargs):
    ActivityLog.objects.create(
        user=user,
        action_type="Logout",
        colour="danger",
        description=f"{user.username} logged out",
    )

@receiver(post_save, sender=RentPayment)
def rent_payment(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
        user=instance.lease.tenant.user.user,
        entity_type="Finance",
        entity_id=instance.id,
        colour="primary",
        description=f"Made a Rent Payment",
        )

        ActivityLog.objects.create(
        user=instance.lease.tenant.building_owner.user.user if instance.lease.tenant.building_owner else instance.lease.tenant.company.user.user,
        entity_type="Finance",
        entity_id=instance.id,
        colour="primary",
        description=f"Received a Rent Payment",
        ip_address="rent-payment-history"
        )

@receiver(post_save, sender=House)
def add_house(sender, instance, created, **kwargs):
    ActivityLog.objects.create(
        user=instance.building_owner.user.user if instance.building_owner else instance.estate.company.user.user,
        action_type="Create" if created else "Update",
        entity_type="House",
        entity_id=instance.id,
        colour="dark",
        description=f"Added a House" if created else "Updated a House",
        ip_address="house-details"
    )

@receiver(pre_delete, sender=House)
def delete_house(sender, instance, **kwargs):
    del_instance = ActivityLog.objects.filter(entity_id=instance.id, entity_type="House").last()
    del_instance.ip_address = None
    del_instance.save()

    ActivityLog.objects.create(
        user=instance.building_owner.user.user if instance.building_owner else instance.estate.company.user.user,
        action_type="Delete",
        entity_type="House",
        entity_id=instance.id,
        colour="error",
        description=f"Deleted a House",
    )

@receiver(post_save, sender=Apartment)
def add_apartment(sender, instance, created, **kwargs):
    ActivityLog.objects.create(
        user=instance.house.building_owner.user.user if instance.house.building_owner else instance.house.estate.company.user.user,
        action_type="Create" if created else "Update",
        entity_type="Apartment",
        entity_id=f"{instance.apartment_number},{instance.house.id}",
        colour="dark",
        description=f"Added an Apartment" if created else "Updated an Apartment",
        ip_address="apartment-details"
    )

@receiver(post_save, sender=WorkOrder)
def workorder(sender, instance, created, **kwargs):
    description = None
    ip_address = None
    if instance.status == 'open':
        description = "Opened a Request"
        ip_address = "open_request"
    elif instance.status == 'in_progress':
        description = "Assigned a Request"
        ip_address = "in_progress_request"
    elif instance.status == 'completed':
        description = "Completed a Request"
        ip_address = "completed_request"
    elif instance.status == 'closed':
        description = 'Cancelled a Request'
        ip_address = "closed_request"
    
    ActivityLog.objects.create(
        user=instance.apartment.tenant_apartment.user.user if created else instance.apartment.tenant_apartment.building_owner.user.user if instance.apartment.tenant_apartment.building_owner else instance.apartment.tenant_apartment.estate.company.user.user,
        action_type="Create" if created else "Update",
        entity_type="WorkOrder",
        entity_id=instance.id,
        colour="secondary",
        description=f"Added a Request" if created else description,
        ip_address=ip_address
    )