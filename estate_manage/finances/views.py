from django.shortcuts import render, redirect
from django.contrib import messages
from leaseAgreements.models import LeaseAgreement
from users.views import check_network_connection
from .forms import RentPaymentForm
from .models import Receipt
from .utils import generate_rent_receipt_image


def rent_payment_portal(request, pk):
    tenant = request.user.profile.tenant
    leaseagreement = tenant.lease_agreements.all().first()

    if request.method == 'POST':
        form = RentPaymentForm(request.POST, request.FILES, tenant=tenant)
        
        if form.is_valid():
            if check_network_connection():
                payment = form.save(commit=False)

                payment.lease = leaseagreement
                payment.save()
                
                Receipt.objects.create(
                    receipt_type='rent',
                    payment=payment,
                    receipt_file=payment.receipt if payment.receipt else None,
                )

                leaseagreement.deposit_amount = float(leaseagreement.deposit_amount) + float(request.POST['amount'])
                leaseagreement.save()

                messages.success(request, "Successfully processed your Rent Payment. Have a nice day!")
                return redirect("payment-history", pk=request.user.profile)
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

def generate_rent_receipt(request, pk):
    redirect_url = request.GET.get("redirect")
    receipt = Receipt.objects.get(id=pk)
    designation = request.user.profile

    generate_rent_receipt_image(
        receipt_number=receipt.receipt_number,
        payment_method=receipt.payment.payment_method,
        house=receipt.payment.lease.apartment.house,
        apartment=receipt.payment.lease.apartment,
        amount=receipt.payment.amount,
        balance=receipt.payment.balance,
        generated_on=receipt.payment.payment_date,
        tenant=None if designation.designation == "tenant"  else receipt.payment.lease.tenant
    )

    messages.success(request, "Rent Receipt sent to your Inbox and Downloads.")
    return redirect(f"{redirect_url}", pk=request.user.profile)
