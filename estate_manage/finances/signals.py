from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RentPayment


@receiver(post_save, sender=RentPayment)
def send_tenant_rent_payment_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Rent Payment Confirmation'
        message = f"""
Dear {instance.lease.tenant},

We have successfully processed your rent payment for the property at {instance.lease.apartment.house} : {instance.lease.apartment}.

Payment Details:
- Amount Paid: ${instance.amount}
- Payment Date: {instance.payment_date}
- Payment Method: {instance.payment_method.title()}
- Apartment Balance: {instance.lease.due_amount()}

If you have any questions or need assistance, please reach out to us at 07033327493.

Thank you for your prompt payment.

Best regards,
EstateManage.
"""
        from_email = settings.EMAIL_HOST_USER
        receipent = [f"{instance.lease.tenant.email}"]
        send_mail(subject, message, from_email, receipent, fail_silently=False)


@receiver(post_save, sender=RentPayment)
def send_building_owner_rent_payment_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Rent Payment Confirmation'
        message = f"""
Dear {instance.lease.tenant.building_owner},

We are pleased to inform you that we have received a rent payment for the property at {instance.lease.apartment.house} : {instance.lease.apartment}.

Payment Details:
- Tenant Name: {instance.lease.tenant}
- Amount Paid: ${instance.amount}
- Payment Date: {instance.payment_date}
- Payment Method: {instance.payment_method.title()}
- Apartment Balance: ${instance.lease.due_amount()}

If you need further details or have any questions, please contact us at 07033327493.

Thank you for your attention.

Best regards,
EstateManage.
"""
        from_email = settings.EMAIL_HOST_USER
        receipent = [f"{instance.lease.tenant.building_owner.contact_email}"]
        send_mail(subject, message, from_email, receipent, fail_silently=False)

