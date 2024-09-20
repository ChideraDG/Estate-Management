from django.db import models
from django.utils import timezone
from tenants.models import Tenant
from apartments.models import Apartment

class LeaseAgreement(models.Model):
    """
    A model representing a lease agreement between a tenant and a house.

    Attributes
    ----------
    tenant : ForeignKey
        A reference to the tenant involved in the lease agreement.
    house : ForeignKey
        A reference to the house involved in the lease agreement.
    start_date : DateField
        The date when the lease starts.
    end_date : DateField
        The date when the lease ends.
    rent_amount : DecimalField
        The amount of rent to be paid by the tenant.
    deposit_amount : DecimalField
        The deposit amount required for the lease.
    payment_schedule : CharField
        The schedule of payments (e.g., monthly, quarterly, annually).
    lease_terms : TextField
        The terms and conditions of the lease agreement.
    agreement_signed : BooleanField
        Indicates whether the lease agreement has been signed.
    date_signed : DateTimeField
        The date and time when the lease agreement was signed.
    """

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='lease_agreements')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='lease_agreements', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_schedule = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ])
    terms_and_conditions = models.TextField()
    agreement_signed = models.BooleanField(default=False)
    date_signed = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date_signed']
        
    def save(self, *args, **kwargs):
        # Check if the agreement is signed and date_signed is not set
        if self.agreement_signed and self.date_signed is None:
            self.date_signed = timezone.now()  # Automatically set to current time
        
        # Call the parent class's save method
        super(LeaseAgreement, self).save(*args, **kwargs)
        
    def __str__(self):
        """
        Returns a string representation of the Lease Agreement.

        Returns
        -------
        str
            A string indicating the house and tenant associated with the lease agreement.
        """
        return f'Lease Agreement for {self.apartment} by {self.tenant}'

    def is_active(self):
        """
        Check if the lease agreement is currently active.

        Returns
        -------
        bool
            True if the lease agreement is active (i.e., today's date is between the start and end dates).
        """
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def days_remaining(self):
        """
        Calculate the number of days remaining until the end of the lease agreement.

        Returns
        -------
        int
            The number of days remaining until the lease ends. If the lease has ended, returns 0.
        """
        today = timezone.now().date()
        if today > self.end_date:
            return 0
        remaining_days = (self.end_date - today).days
        return remaining_days
    
    def due_amount(self) -> float:
        """
        Calculate the remaining due amount after subtracting the deposit.

        Returns:
            float: The remaining due amount after subtracting the deposit.
        """
        return float(float(self.rent_amount) - float(self.deposit_amount))

    
class Reminder(models.Model):
    """
    Represents a reminder associated with a lease agreement.

    Attributes
    ----------
    lease : ForeignKey
        The lease agreement that the reminder is associated with.
    reminder_date : date
        The date on which the reminder is scheduled to be sent.
    message : str
        The content of the reminder message.
    """

    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE, related_name='reminders')
    reminder_date = models.DateField()
    message = models.TextField()

    def __str__(self):
        return f"Reminder: {self.lease} - {self.reminder_date}"
