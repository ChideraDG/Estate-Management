from django import forms
from .models import WorkOrder

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