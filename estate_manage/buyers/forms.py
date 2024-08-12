from django.forms import ModelForm
from django import forms
from .models import Buyer

class BuyerForm(ModelForm):
    class Meta:
        model = Buyer
        fields = [
            'full_name', 'email', 'phone_number', 'address', 'country', 'state', 'city', 'budget',
            'preferred_property_type', 'preferred_location', 'notes'
        ]

        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'budget': 'Budget',
            'preferred_property_type': 'Preferred Property Type',
            'preferred_location': 'Preferred Location',
            'notes': 'Notes',
        }

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City'}),
            'preferred_location': forms.TextInput(attrs={'placeholder': 'Enter location'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter notes',
                                                        'cols': 45,
                                                        'rows': 8,
                                                        }),
        }