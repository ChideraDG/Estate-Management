from django.db import models
from apartments.models import Apartment
from leaseAgreements.models import LeaseAgreement


class RentPayment(models.Model):
    """This model represents individual rent payments made by tenants."""

    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE, related_name='rent_payments')
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, 
                                      choices=[
                                          ('bank_transfer', 'Bank Transfer'), 
                                          ('cash', 'Cash'), 
                                          ('online', 'Online Payment')
                                          ])
    receipt = models.FileField(upload_to='rent_receipts/', null=True, blank=True)
    
    def __str__(self):
        return f"Rent Payment: {self.lease} - {self.amount} on {self.payment_date}"


class Expense(models.Model):
    """This model tracks the various expenses incurred in managing properties."""

    EXPENSE_CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('taxes', 'Taxes'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]
    
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    receipt = models.FileField(upload_to='expense_receipts/', null=True, blank=True)
    
    def __str__(self):
        return f"Expense: {self.category} - {self.amount} on {self.date}"
    

class FinancialReport(models.Model):
    """This model handles the generation and storage of financial reports, 
    such as monthly and annual reports, profit and loss statements, and budget tracking."""

    report_type = models.CharField(max_length=50, 
                                   choices=[
                                       ('monthly', 'Monthly'), 
                                       ('annual', 'Annual'), 
                                       ('profit_loss', 'Profit & Loss'), 
                                       ('budget', 'Budget')])
    report_date = models.DateField()
    generated_on = models.DateTimeField(auto_now_add=True)
    total_income = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2)
    report_file = models.FileField(upload_to='financial_reports/', null=True, blank=True)
    
    def __str__(self):
        return f"Financial Report: {self.report_type} - {self.report_date}"


class PaymentReminder(models.Model):
    """This model is used to schedule and manage automated payment reminders for tenants."""

    lease = models.ForeignKey(LeaseAgreement, on_delete=models.CASCADE, related_name='payment_reminders')
    reminder_date = models.DateField()
    message = models.TextField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment Reminder: {self.lease} on {self.reminder_date}"
    

class Receipt(models.Model):
    """This model generates and stores receipts for both rent payments and expenses."""

    receipt_type = models.CharField(max_length=50, choices=[('rent', 'Rent'), ('expense', 'Expense')])
    payment = models.ForeignKey(RentPayment, on_delete=models.CASCADE, related_name='receipts', null=True, blank=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='receipts', null=True, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    receipt_file = models.FileField(upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f'Receipt #{self.receipt_number}'
    
    def save(self, *args, **kwargs):
        """Override the save method to generate a unique receipt number."""
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
        super().save(*args, **kwargs)

    def generate_receipt_number(self):
        """Generate a unique receipt number."""
        last_receipt = Receipt.objects.order_by('id').last()
        if last_receipt:
            new_number = int(last_receipt.receipt_number.split('-')[1]) + 1
        else:
            new_number = 1
        return f'ESM-{new_number:08}'

