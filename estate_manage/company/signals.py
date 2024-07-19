from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile as userProfile
from .models import Profile


@receiver(post_save, sender=userProfile)
def createCompanyProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.designation == 'company':
            Profile.objects.create(
                owner=user,
                name=user.name,
            )
