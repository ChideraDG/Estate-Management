from django import forms
from .models import RentPayment

class RentPaymentForm(forms.ModelForm):
    """
    A form for creating and updating rent payments.
    """

    class Meta:
        model = RentPayment
        fields = ['lease', 'amount', 'payment_method', 'receipt']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control', 'id': 'id_payment_method'}),
            'receipt': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_receipt'}),
        }

    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        super().__init__(*args, **kwargs)

        self.fields['lease'].initial = tenant.lease_agreements.all().first()
        self.fields['lease'].widget.attrs['disabled'] = True
        self.fields['lease'].widget.attrs['class'] = 'form-control'
        self.fields['lease'].label = 'Lease Agreement'
        self.fields['lease'].help_text = 'Select the lease agreement for this payment.'

        for name, field in self.fields.items():
            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({'min': '0'})
