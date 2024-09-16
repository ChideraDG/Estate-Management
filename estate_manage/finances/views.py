from django.shortcuts import render, redirect
from django.contrib import messages
from leaseAgreements.models import LeaseAgreement
from .forms import RentPaymentForm


def rent_payment_portal(request, pk):
    tenant = request.user.profile.tenant
    leaseagreement = tenant.lease_agreements.all().first()

    if request.method == 'POST':
        form = RentPaymentForm(request.POST, request.FILES, tenant=tenant)
        
        if form.is_valid():
            payment = form.save(commit=False)

            leaseagreement.deposit_amount = leaseagreement.deposit_amount + int(request.POST['amount'])
            leaseagreement.save()

            payment.lease = leaseagreement
            payment.save()

            messages.success(request, "Successfully processed your Rent Payment. Have a nice day!")
            return redirect("dashboard-T", pk=request.user.profile)
        else:
            for errors in form.errors.items():
                print(errors)
    else:
        form = RentPaymentForm(tenant=tenant)

    context = {
        "menu": "tb",
        "s_menu": "trpm",
        "leaseagreement": leaseagreement,
        "tenant": tenant,
        "form": form,
    }
    return render(request, 'finances/rent_payment_portal.html', context)
