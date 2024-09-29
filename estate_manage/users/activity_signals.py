from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from finances.models import RentPayment
from houses.models import House
from apartments.models import Apartment
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
        user=instance.lease.tenant.building_owner.user.user,
        entity_type="Finance",
        entity_id=instance.id,
        colour="primary",
        description=f"Received a Rent Payment",
        ip_address="rent-payment-history"
        )

@receiver(post_save, sender=House)
def add_house(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
        user=instance.building_owner.user.user,
        entity_type="House",
        entity_id=instance.id,
        colour="dark",
        description=f"Added a House",
        ip_address="house-details"
        )

@receiver(post_save, sender=Apartment)
def add_apartment(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
        user=instance.house.building_owner.user.user,
        entity_type="Apartment",
        entity_id=f"{instance.apartment_number},{instance.house.id}",
        colour="dark",
        description=f"Added an Apartment",
        ip_address="apartment-details"
        )
