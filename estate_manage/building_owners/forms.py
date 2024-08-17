import re
from django.forms import ModelForm
from django import forms
from django.contrib import messages
from .models import BuildingOwner
from django.core.exceptions import ValidationError


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
                  'is_visible', 'investment_strategy', 'tax_id', 'notes']
        
        labels = {
            'building_owner_name': 'Building Owner Name',
            'contact_email': 'Contact Email',
            'contact_phone': 'Contact Phone',
            'address': 'Address',
            'profile_pics': 'Profile Picture',
            'city': 'City',
            'country': 'Country',
            'state': 'State',
            'is_visible': 'Private Account',
            'investment_strategy': 'Investment Strategy',
            'tax_id': 'Tax ID',
            'notes': 'Notes',
        }

        widgets = {
            'contact_phone': forms.TextInput(attrs={
                'placeholder': 'Enter contact phone number',
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Enter address',
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Enter city',
                'class': 'form-control'
            }),
            'country': forms.Select(attrs={
                'placeholder': 'Select country',
                'class': 'form-control'
            }),
            'state': forms.Select(attrs={
                'placeholder': 'Select state',
                'class': 'form-control'
            }),
            'investment_strategy': forms.Select(choices=BuildingOwner.DESIGNATION, attrs={
                'class': 'form-control'
            }),
            'tax_id': forms.TextInput(attrs={
                'placeholder': 'Enter tax id',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Enter notes',
                'cols': 45,
                'rows': 6,
                'class': 'form-control'
            }),
            'is_visible': forms.NullBooleanSelect(attrs={
                'class': 'form-control'
            }),
            'contact_email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'class': 'form-control',
                'required': True
            }),
            'building_owner_name': forms.TextInput(attrs={
                'placeholder': 'Enter contact email',
                'class': "form-control"
            }),
            'profile-pics': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BuildingOwnerForm, self).__init__(*args, **kwargs)

    def clean_contact_phone(self):
        contact_phone = self.cleaned_data.get('contact_phone')

        # Example: Ensure the phone number is numeric and has 10 digits
        if not contact_phone.isdigit() or len(contact_phone) <=10:
            messages.error(self.request, "Enter a valid Phone Number.")
            raise ValidationError('Enter a valid Phone number.')
        
        return contact_phone
    
    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')

        # Check if email is not empty (although required=True should handle this)
        if not email:
            messages.error(self.request, "Email address is required.")
            raise ValidationError("Email address is required.")
        
        # Ensure email format is correct
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messages.error(self.request, "Invalid email format.")
            raise ValidationError("Invalid email format.")
        
        # Example: Check if email contains a specific word
        if 'spam' in email:
            messages.error(self.request, "Email address cannot contain the word 'spam'.")
            raise ValidationError("Email address cannot contain the word 'spam'.")

        return email      
    
    def clean_building_owner_name(self):
        building_owner_name = self.cleaned_data.get('building_owner_name')

        if not building_owner_name:
            messages.error(self.request, "Owner name is Required")
            raise ValidationError("Owner name is Required")
