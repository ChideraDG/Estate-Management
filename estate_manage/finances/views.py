from django.shortcuts import render, redirect
from django.contrib import messages
from leaseAgreements.models import LeaseAgreement
from users.views import check_network_connection
from .forms import RentPaymentForm
from .models import Receipt


def rent_payment_portal(request, pk):
    tenant = request.user.profile.tenant
    leaseagreement = tenant.lease_agreements.all().first()

    if request.method == 'POST':
        form = RentPaymentForm(request.POST, request.FILES, tenant=tenant)
        
        if form.is_valid():
            if check_network_connection():
                payment = form.save(commit=False)

                leaseagreement.deposit_amount = leaseagreement.deposit_amount + int(request.POST['amount'])
                leaseagreement.save()

                payment.lease = leaseagreement
                payment.save()
                
                Receipt.objects.create(
                    receipt_type='rent',
                    payment=payment,
                    receipt_file=payment.receipt if payment.receipt else None,
                )

                messages.success(request, "Successfully processed your Rent Payment. Have a nice day!")
                return redirect("dashboard-T", pk=request.user.profile)
            else:
                messages.error(request, "Network connection failed. Please try again.")
                return redirect("rent-payment", pk=request.user)
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
