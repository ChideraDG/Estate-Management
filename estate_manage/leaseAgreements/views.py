from django.shortcuts import render
from .models import LeaseAgreement
from .forms import LeaseAgreementForm

def lease_agreements(request, type, pk):
    active_menu = request.GET.get("active_menu", "")
    active_sub_menu = request.GET.get("active_sub_menu", "")
    lease_update = request.GET.get("lease_update", False)
    tenant = request.GET.get("tenant_id", "")
    lease_agreement = LeaseAgreement.objects.filter(tenant=tenant).first()
    profile = request.user.profile
    tenants = None
    if profile.designation == "building_owner":
        tenants = profile.building_owner.tenants.all()
        agreements = LeaseAgreement.objects.filter(tenant__in=tenants)

    if request.method == "POST":
        form = LeaseAgreementForm(request.POST, request.FILES, instance=lease_agreement)
        if form.is_valid():
            agreement = form.save()
        else:
            pass
    else:
        form = LeaseAgreementForm(instance=lease_agreement)

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
        "lease_update": lease_update,
    }
    return render(request, 'leaseAgreements/agreements.html', context)
