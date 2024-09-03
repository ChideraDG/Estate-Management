from django import forms
from .models import LeaseAgreement
from tenants.models import Tenant

class LeaseAgreementForm(forms.ModelForm):
    class Meta:
        model = LeaseAgreement
        fields = [
            'tenant', 'apartment', 'start_date', 'end_date', 
            'rent_amount', 'deposit_amount', 'payment_schedule', 
            'agreement_document', 'terms_and_conditions', 
            'agreement_signed', 'date_signed'
        ]
        widgets = {
            'tenant': forms.Select(attrs={'placeholder': 'Select Tenant'}),
            'apartment': forms.Select(attrs={'placeholder': 'Select Apartment'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'End Date'}),
            'rent_amount': forms.NumberInput(attrs={'placeholder': 'Enter Rent Amount'}),
            'deposit_amount': forms.NumberInput(attrs={'placeholder': 'Enter Deposit Amount'}),
            'payment_schedule': forms.Select(attrs={'placeholder': 'Select Payment Schedule'}),
            'agreement_document': forms.ClearableFileInput(attrs={'placeholder': 'Upload Agreement Document'}),
            'terms_and_conditions': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Terms and Conditions'}),
            'agreement_signed': forms.NullBooleanSelect,
            'date_signed': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Date Signed'}),
        }

    def __init__(self, *args, **kwargs):
        building_owner = kwargs.pop('building_owner', None)
        super(LeaseAgreementForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})

        # Filter the queryset based on the building_owner
        if building_owner:
            self.fields['tenant'].queryset = Tenant.objects.filter(building_owner=building_owner)