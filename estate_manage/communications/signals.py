from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from building_owners.models import BuildingOwner
from users.models import Profile
from . import bo_view, tenant_view

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if user.profile.designation == 'building_owner':
        # The total unread messages across all tenants
        unread_total = bo_view.bo_get_unread(request)
        Profile.objects.filter(username=request.user).update(unread_messages=unread_total)
    elif user.profile.designation == 'tenant':
        if user.profile.tenant.building_owner:
            unread_total = tenant_view.tenant_get_unread(request)
            Profile.objects.filter(username=request.user).update(unread_messages=unread_total)  
