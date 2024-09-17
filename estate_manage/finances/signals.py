from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RentPayment


@receiver(post_save, sender=RentPayment)
def send_tenant_rent_payment(sender, instance, created, **kwargs):
    if created:
        subject = 'Rent Payment Confirmation'
        message = f"""
Dear {instance.lease.tenant},

We have successfully processed your rent payment for the property at {instance.lease}.

Payment Details:
- Amount Paid: {instance.amount}
- Payment Date: {instance.payment_date}
- Payment Method: {instance.get_payment_method.display()}

Attached is your receipt for this transaction. If you have any questions or need assistance, please reach out to us at 07033327493.

Thank you for your prompt payment.

Best regards,
EstateManage.
"""