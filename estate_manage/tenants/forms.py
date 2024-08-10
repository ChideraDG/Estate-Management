from django.forms import ModelForm
from django import forms
from .models import Tenant

class TenantForm(ModelForm):
    class Meta:
        model = Tenant
        fields = [
            'first_name', 'last_name', 'email', 'phone_number','country', 'state', 'city', 'profile_picture', 'move_in_date', 'lease_start_date',
            'lease_end_date', 'monthly_rent', 'deposit_amount', 'lease_term', 'payment_status', 'emergency_contact_name',
            'emergency_contact_number', 'employment_status', 'occupation', 'notes'
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
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'city': forms.TextInput(attrs={ 'placeholder': 'Enter city'}),
            'country': forms.Select(attrs={ 'placeholder': 'Select country'}),
            'state': forms.Select(attrs={ 'placeholder': 'Select state'}),
            'profile_picture': forms.FileInput(),
            'move_in_date': forms.DateInput(attrs={'placeholder': 'Enter Move In Date', 'type': 'date'}),
            'lease_start_date': forms.DateInput(attrs={'placeholder': 'Enter Lease Start Date', 'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'placeholder': 'Enter Lease End Date', 'type': 'date'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Enter occupation'}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Name'}),
            'emergency_contact_number': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Number'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter note',
                                                        'cols': 45,
                                                        'rows': 8,
                                                        }),

        }
        