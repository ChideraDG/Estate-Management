import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from documents.models import Document
from .models import LeaseAgreement
from .forms import LeaseAgreementForm

@login_required(login_url='login')
def lease_agreements(request, type, pk):
    menu = request.GET.get("menu", "tm")
    s_menu = request.GET.get("s_menu", "ta")
    profile = request.user.profile
    tenants = None
    if profile.designation == "building_owner":
        tenants = profile.building_owner.tenants.all()
        agreements = LeaseAgreement.objects.filter(tenant__in=tenants)

    lease_update = request.GET.get("lease_update", False)
    if lease_update:
        tenant = request.GET.get("tenant_id", "")
        lease_agreement = LeaseAgreement.objects.filter(tenant=tenant).first()
        if request.method == "POST":
            form = LeaseAgreementForm(request.POST, request.FILES, instance=lease_agreement)
            files = request.FILES.getlist('docs')

            if form.is_valid():
                agreement = form.save()

                for file in files:
                    Document.objects.create(
                        title=agreement.payment_schedule,
                        file=file,
                        document_type='lease_agreement',
                        uploaded_by=request.user,
                        related_apartment=agreement.apartment,
                        related_lease=agreement
                    )

                return redirect('agreements', pk=pk, type=type)
            else:
                pass
        else:
            form = LeaseAgreementForm(instance=lease_agreement)
    else:
        form = ""

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
    }
    context = {
        "menu": menu,
        "s_menu": s_menu,
        "template_routes": template_routes.get(profile.designation),
        "agreements": agreements,
        "tenants": tenants,
        "type": type,
        "form": form,
        "lease_update": lease_update,
    }
    return render(request, 'leaseAgreements/agreements.html', context)

@login_required(login_url='login')
def agreements_details(request, type, pk, agreement_id):
    menu = request.GET.get("menu", "tm")
    s_menu = request.GET.get("s_menu", "ta")
    profile = request.user.profile
    agreement = LeaseAgreement.objects.get(id=agreement_id)

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
    }
    context = {
        'user': request.user.profile,
        'menu': menu,
        's_menu': s_menu,
        'agreement': agreement,
        'type': type,
        'template_routes': template_routes.get(profile.designation),
    }
    return render(request, 'leaseAgreements/agreements_details.html', context)

@login_required(login_url='login')
def update_agreement(request, type, pk, agreement_id):
    menu = request.GET.get("menu", "tm")
    s_menu = request.GET.get("s_menu", "ta")
    profile = request.user.profile
    agreement = LeaseAgreement.objects.get(id=agreement_id)

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
    }

    if request.method == 'POST':
        form = LeaseAgreementForm(request.POST, instance=agreement)
        files = request.FILES.getlist('docs')
        
        lease = LeaseAgreement.objects.filter(id=agreement_id)
        lease.update(
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            rent_amount=request.POST['rent_amount'],
            deposit_amount=request.POST['deposit_amount'],
            payment_schedule=request.POST['payment_schedule'],
            terms_and_conditions=request.POST['terms_and_conditions'],
            agreement_signed=True if request.POST['agreement_signed'].lower() == 'true' else False,
        )

        if request.POST['date_signed']:
            if lease.first().agreement_signed:
                lease.update(date_signed=request.POST['date_signed'])
        if lease.first().agreement_signed and lease.first().date_signed is None:
            lease.update(date_signed=timezone.now())
        if not lease.first().agreement_signed:
            lease.update(date_signed=None)

        for file in files:
            Document.objects.create(
                title=agreement.payment_schedule,
                file=file,
                document_type='lease_agreement',
                uploaded_by=request.user,
                related_apartment=agreement.apartment,
                related_lease=agreement
            )
        
        return redirect('agreement-detail', pk=profile, type=type, agreement_id=agreement.id)
    else:
        form = LeaseAgreementForm(instance=agreement)

    context = {
        'profile': profile,
        'menu': menu,
        's_menu': s_menu,
        'agreement': agreement,
        'type': type,
        'template_routes': template_routes.get(profile.designation),
        'form': form,
    }
    return render(request, 'leaseAgreements/update_agreement.html', context)