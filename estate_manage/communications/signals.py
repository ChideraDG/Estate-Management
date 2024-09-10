from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from building_owners.models import BuildingOwner
from . import bo_views

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if user.profile.designation == 'building owner':
        # The total unread messages across all tenants
        unread_total = bo_views.get_unread(request)
        BuildingOwner.objects.filter(id=request.user.profile.building_owner.id).update(unread_messages=unread_total)
