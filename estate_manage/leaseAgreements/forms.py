from django import forms
from django.db.models import Q
from .models import LeaseAgreement
from tenants.models import Tenant
from apartments.models import Apartment

class LeaseAgreementForm(forms.ModelForm):
    class Meta:
        model = LeaseAgreement
        fields = [
            'tenant', 'apartment', 'start_date', 'end_date', 
            'rent_amount', 'deposit_amount', 'payment_schedule', 
            'terms_and_conditions', 'agreement_signed', 'date_signed'
        ]
        widgets = {
            'tenant': forms.Select(attrs={'placeholder': 'Select Tenant'}),
            'apartment': forms.Select(attrs={'placeholder': 'Select Apartment'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'End Date'}),
            'rent_amount': forms.NumberInput(attrs={'placeholder': 'Enter Rent Amount'}),
            'deposit_amount': forms.NumberInput(attrs={'placeholder': 'Enter Deposit Amount'}),
            'payment_schedule': forms.Select(attrs={'placeholder': 'Select Payment Schedule'}),
            'terms_and_conditions': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Terms and Conditions'}),
            'agreement_signed': forms.NullBooleanSelect,
            'date_signed': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Date Signed'}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaseAgreementForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})
