from django.forms import ModelForm
from django import forms
from . models import House

class HouseForm(ModelForm):
    """
    A form for creating and updating House instances.

    Attributes:
        model (House): The model associated with the form.
        fields (list): The list of fields to be included in the form.
        labels (dict): Custom labels for the form fields.
        widgets (dict): Custom widgets for the form fields.

    Meta:
        model : House
            The model to which this form is linked.
        fields : list of str
            Fields included in the form: 'house_number', 'address', 'country', 'state', 'city', 
            'house_size', 'number_of_apartments', 'total_floor_number', 'house_garage_space', 
            'yard_size', 'renovation_year', 'condition', 'features', 'utilities', 
            'sale_price', 'rent_price', 'occupancy_status', 'notes'.
        labels : dict of str
            Custom labels for form fields.
        widgets : dict of forms.Widget
            Custom widgets for form fields.

    Examples:
        >>> form = HouseForm()
        >>> form.is_valid()
    """

    class Meta:
        model = House
        fields = [
            'house_number', 'address', 'country', 'state', 'city', 'house_size', 'number_of_apartments', 
            'total_floor_number', 'house_garage_space', 'yard_size', 'renovation_year', 'condition', 
            'features', 'utilities', 'sale_price', 'rent_price', 'occupancy_status', 'notes'
        ]

        labels = {
            'house_number': 'House Number',
            'address': 'Address',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'house_size': 'House Size (square metres)',
            'number_of_apartments': 'Number of Apartments',
            'total_floor_number': 'Total Floor Number',
            'house_garage_space': 'House Garage Space',
            'yard_size': 'Yard Size (square metres)',
            'renovation_year': 'Renovation Year',
            'condition': 'Condition',
            'features': 'Features',
            'utilities': 'Utilities',
            'sale_price': 'Sale Price',
            'rent_price': 'Rent Price',
            'occupancy_status': 'Occupancy Status',
            'notes': 'Notes',
        }

        widgets = {
            'house_number': forms.NumberInput(attrs={'placeholder': 'Enter House Number'}),
            'address': forms.Textarea(attrs={ 'placeholder': 'Enter address', 'cols': 30, 'rows': 8}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city'}),
            'country': forms.Select(attrs={'placeholder': 'Select country'}),
            'state': forms.Select(attrs={'placeholder': 'Select state'}),
            'utilities': forms.CheckboxSelectMultiple(),
            'features': forms.CheckboxSelectMultiple(),
            'renovation_year': forms.NumberInput(attrs={'value': 1900}),
            'occupancy_status': forms.Select(choices=House.OCCUPANCY, attrs={'placeholder': 'Select occupancy status'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter notes', 'cols': 45, 'rows': 8}),
        }
        