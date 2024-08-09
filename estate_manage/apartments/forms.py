from django.forms import ModelForm
from django import forms
from . models import Apartment

from django.forms import ModelForm
from django import forms
from .models import Apartment

class ApartmentForm(ModelForm):
    """
    A Django form class for creating and editing Apartment instances.

    The form includes fields for apartment details, lease information, and occupancy status.
    It uses Django's built-in form widgets and validation.

    Fields:
        - apartment_number: The unique identifier for the apartment.
        - floor_number: The floor number where the apartment is located.
        - country: The country where the apartment is located.
        - state: The state or province where the apartment is located.
        - city: The city where the apartment is located.
        - apartment_size: The size of the apartment in square meters.
        - number_of_rooms: The number of rooms in the apartment.
        - rent_amount: The monthly rent amount.
        - deposit_amount: The security deposit amount.
        - lease_start_date: The start date of the lease.
        - lease_end_date: The end date of the lease.
        - occupancy_status: The current occupancy status of the apartment.
        - condition: The condition of the apartment.
        - pet_allowed: Whether pets are allowed in the apartment.
        - notes: Additional notes about the apartment.
    """

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
            'notes': 'Notes',
        }

        widgets = {
            'apartment_number': forms.NumberInput(attrs={'placeholder': 'Enter Apartment Number'}), 
            'city': forms.TextInput(attrs={ 'placeholder': 'Enter city'}),
            'country': forms.Select(attrs={ 'placeholder': 'Select country'}),
            'state': forms.Select(attrs={ 'placeholder': 'Select state'}),
            'lease_start_date': forms.DateInput(attrs={'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter notes',
                                                        'cols': 45,
                                                        'rows': 8,
                                                        }),
        }
