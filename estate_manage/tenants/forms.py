from django.forms import ModelForm
from django import forms
from .models import Tenant
import re
from django.contrib import messages
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class TenantForm(ModelForm):
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                message="Phone number must be entered in the format: '08012345678' or '+2348012345678'. Up to 15 digits allowed."
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
        label='Phone Number')
        
    class Meta:
        model = Tenant
        fields = [
            'first_name', 'last_name', 'email', 'phone_number','country', 'state', 'city', 'profile_picture', 'move_in_date', 'lease_start_date',
            'lease_end_date', 'monthly_rent', 'deposit_amount', 'lease_term', 'payment_status', 'emergency_contact_name',
            'emergency_contact_number', 'employment_status', 'occupation'
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'profile_picture': 'Profile Picture',
            'move_in_date': 'Move In Date',
            'lease_start_date': 'Lease Start Date',
            'lease_end_date': 'Lease End Date',
            'monthly_rent': 'Monthly Rent',
            'deposit_amount': 'Deposit Amount',
            'lease_term': 'Lease Term',
            'payment_status': 'Payment Status',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_number': 'Emergency Contact Phone Number',
            'employment_status': 'Employment Status',
            'occupation': 'Occupation',
            'notes': 'Notes',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name',  'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name',  'class': 'form-control',}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email',  'class': 'form-control',}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number',  'class': 'form-control',}),
            'city': forms.TextInput(attrs={ 'placeholder': 'Enter city',  'class': 'form-control',}),
            'country': forms.Select(attrs={ 
                'placeholder': 'Select country',
                'class': 'form-control',
                'id': 'id_country',}),
            'state': forms.Select(attrs={
                 'placeholder': 'Select state',
                   'class': 'form-control',
                    'id': 'id_state',}),
            'profile_picture': forms.FileInput(attrs={ 'class': 'form-control',}),
            'move_in_date': forms.DateInput(attrs={'placeholder': 'Enter Move In Date', 'type': 'date',  'class': 'form-control',}),
            'lease_start_date': forms.DateInput(attrs={'placeholder': 'Enter Lease Start Date', 'type': 'date',  'class': 'form-control',}),
            'lease_end_date': forms.DateInput(attrs={'placeholder': 'Enter Lease End Date', 'type': 'date',  'class': 'form-control',}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Enter occupation',  'class': 'form-control',}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
            'lease_term': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'deposit_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_rent': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Name',  'class': 'form-control',}),
            'emergency_contact_number': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Number',  'class': 'form-control',}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter note',
                                                        'cols': 45,
                                                        'rows': 8,
                                                        'class': 'form-control',
                                                        }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TenantForm, self).__init__(*args, **kwargs)

    def clean_contact_phone(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Example: Ensure the phone number is numeric and has 10 digits
        if not phone_number.replace("+", "").isdigit() or len(phone_number) <=10:
            messages.error(self.request, "Enter a valid Phone Number.")
            raise ValidationError('Enter a valid Phone number.')
        
        return phone_number
        