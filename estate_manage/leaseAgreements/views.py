from django.shortcuts import render
from .models import LeaseAgreement
from .forms import LeaseAgreementForm

def lease_agreements(request, type, pk):
    active_menu = request.GET.get("active_menu", "")
    active_sub_menu = request.GET.get("active_sub_menu", "")
    profile = request.user.profile

    tenants = None
    if profile.designation == "building_owner":
        tenants = profile.building_owner.tenants.all()
        agreements = LeaseAgreement.objects.filter(tenant__in=tenants)

    if request.method == "POST":
        form = LeaseAgreementForm(request.POST, building_owner=profile.building_owner)
        if form.is_valid():
            form.save()
        else:
            pass
    else:
        form = LeaseAgreementForm(building_owner=profile.building_owner)

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
    }
    context = {
        "active_menu": active_menu,
        "active_sub_menu": active_sub_menu,
        "template_routes": template_routes.get(profile.designation),
        "agreements": agreements,
        "tenants": tenants,
        "form": form,
    }
    return render(request, 'leaseAgreements/agreements.html', context)
