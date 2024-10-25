from django import forms
from .models import WorkOrder, ServiceProvider

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['apartment', 'description', 'notes']
        
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue you are facing'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional notes (optional)'}),
        }

        labels = {
            'apartment': 'Apartment',
            'description': 'Issue Description',
            'notes': 'Additional Notes (Optional)',
        }

    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        super().__init__(*args, **kwargs)

        self.fields['apartment'].initial = tenant.apartment
        self.fields['apartment'].widget.attrs['disabled'] = True
        self.fields['apartment'].widget.attrs['class'] = 'form-control'


class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = [
            'name',
            'contact_person',
            'phone_number',
            'email',
            'address',
            'service_type',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Provider Name', 'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'Contact Person', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'class': 'form-control', 'rows': 3}),
            'service_type': forms.RadioSelect(attrs={'class': 'form-check-input', 'type': 'radio'}),
        }
