from django.shortcuts import render
from .models import LeaseAgreement

def lease_agreements(request, type, pk):
    active_menu = request.GET.get("active_menu", "")
    active_sub_menu = request.GET.get("active_sub_menu", "")
    profile = request.user.profile

    if profile.designation == "building_owner":
        agreements = LeaseAgreement.objects.filter(tenant__in=profile.building_owner.tenants.all())

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
    }
    context = {
        "active_menu": active_menu,
        "active_sub_menu": active_sub_menu,
        "template_routes": template_routes.get(profile.designation),
        "agreements": agreements,
    }
    return render(request, 'leaseAgreements/agreements.html', context)
