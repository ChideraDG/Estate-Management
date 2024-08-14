from django.forms import ModelForm
from django import forms
from .models import BuildingOwner

class BuildingOwnerForm(ModelForm):
    """
    A Django form class for creating and editing BuildingOwner instances.

    The form includes fields for building owner name, contact email, contact phone, 
    address, country, state, city, portfolio size, investment strategy, tax id, and notes.

    Example usage:

    ```
    # Create a new BuildingOwner instance
    form = BuildingOwnerForm()
    if form.is_valid():
        building_owner = form.save()
        print(building_owner.building_owner_name)

    # Edit an existing BuildingOwner instance
    building_owner = BuildingOwner.objects.get(id=1)
    form = BuildingOwnerForm(instance=building_owner)
    if form.is_valid():
        form.save()
    ```

    Attributes:
        model (BuildingOwner): The model that this form is associated with.
        fields (list): A list of field names that should be included in the form.
        labels (dict): A dictionary of labels for each field.
        widgets (dict): A dictionary of widgets for each field.
    """

    class Meta:
        model = BuildingOwner
        fields = ['building_owner_name', 'contact_email', 'contact_phone', 'address', 'profile_pics', 'country', 'state', 'city',
                  'portfolio_size', 'investment_strategy', 'tax_id', 'notes']
        
        labels = {
            'building_owner_name': 'Building Owner Name',
            'contact_email': 'Contact Email',
            'contact_phone': 'Contact Phone',
            'address': 'Address',
            'profile_pics': 'Profile Pics',
            'city': 'City',
            'country': 'Country',
            'state': 'State',
            'portfolio_size': 'Portfolio Size',
            'investment_strategy': 'Investment Strategy',
            'tax_id': 'Tax ID',
            'notes': 'Notes',
        }

        widgets = {
            'building_owner_name': forms.TextInput(attrs={ 'placeholder': 'Enter building owner name'}),
            'contact_email': forms.EmailInput(attrs={ 'placeholder': 'Enter contact email'}),
            'contact_phone': forms.TextInput(attrs={ 'placeholder': 'Enter contact phone number'}),
            'address': forms.TextInput(attrs={ 'placeholder': 'Enter address'}),
            'profile_pics': forms.FileInput,
            'city': forms.TextInput(attrs={ 'placeholder': 'Enter city'}),
            'country': forms.Select(attrs={ 'placeholder': 'Select country'}),
            'state': forms.Select(attrs={ 'placeholder': 'Select state'}),
            'portfolio_size': forms.NumberInput(attrs={'value': '1'}),
            'investment_strategy': forms.Select(choices=BuildingOwner.DESIGNATION),
            'tax_id': forms.TextInput(attrs={ 'placeholder': 'Enter tax id'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter notes',
                                                        'cols': 45,
                                                        'rows': 6,
                                                        }),
        }