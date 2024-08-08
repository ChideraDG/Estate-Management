from django.forms import ModelForm
from django import forms
from . models import Apartment

class ApartmentForm(ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'apartment_number', 'floor_number', 'country', 'state', 'city', 'apartment_size', 'number_of_rooms', 'rent_amount',
            'deposit_amount', 'lease_start_date', 'lease_end_date', 'occupancy_status', 'condition', 'pet_allowed', 'notes'
        ]

        labels = {
            'apartment_number': 'Apartment Number',
            'floor_number': 'Floor Number', 
            'country': 'Country', 
            'state': 'State', 
            'city': 'City', 
            'apartment_size': 'Apartment Size (Square metres)', 
            'number_of_rooms ': 'Number of Rooms', 
            'rent_amount': 'Rent Amount',
            'deposit_amount': 'Deposit Amount', 
            'lease_start_date': 'Lease Start Date', 
            'lease_end_date': 'Lease End Date', 
            'occupancy_status': 'Occupancy Status', 
            'condition': 'Condition', 
            'pet_allowed': 'Pets Allowed', 
            'note': 'Note,'
        }

        widgets = {
            'apartment_number': forms.NumberInput(attrs={'placeholder': 'Enter Apartment Number'}), 
            'city': forms.TextInput(attrs={ 'placeholder': 'Enter city'}),
            'country': forms.Select(attrs={ 'placeholder': 'Select country'}),
            'state': forms.Select(attrs={ 'placeholder': 'Select state'}),
            'lease_start_date': forms.DateInput(attrs={'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'placeholder': 'Enter note',
                                                        'cols': 45,
                                                        'rows': 8,
                                                        }),
        }