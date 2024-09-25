from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from .models import ActivityLog


@receiver(signal=user_logged_in)
def user_login(sender, request, user, **kwargs):
    ActivityLog.objects.create(
        user=user,
        action_type="Login",
        colour="success",
        description=f"{user.username} logged in.",
    )

@receiver(signal=user_logged_out)
def user_logout(sender, request, user, **kwargs):
    ActivityLog.objects.create(
        user=user,
        action_type="Logout",
        colour="danger",
        description=f"{user.username} logged out.",
    )