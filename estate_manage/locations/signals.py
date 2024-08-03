from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import City
from estates.models import Estate


@receiver(post_save, sender=Estate)
def estate(sender, instance, created, **kwargs):
    if created:
        if instance.city:
            if not City.objects.get(name=instance.city).exists():
                City.objects.create(country=instance.country)