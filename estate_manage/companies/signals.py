from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile
from .models import Company


@receiver(post_save, sender=Profile)
def createCompanyProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.designation == 'company':
            Company.objects.create(
                owner=user,
                name=user.name,
                email=user.email,
            )
