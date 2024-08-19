from django.forms import ModelForm
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import House

class HouseForm(ModelForm):
    """
    A Django form class for creating and editing House instances.

    The form includes fields for house number, address, country, state, city, house size, 
    number of apartments, number of floors, garage space, yard size, renovation year, condition, 
    features, utilities, sale price, rent price, occupancy status, and notes.

    Example usage:

    ```
    # Create a new House instance
    form = HouseForm()
    if form.is_valid():
        house = form.save()
        print(house.house_number)

    # Edit an existing House instance
    house = House.objects.get(id=1)
    form = HouseForm(instance=house)
    if form.is_valid():
        form.save()
    ```

    Attributes:
        model (House): The model that this form is associated with.
        fields (list): A list of field names that should be included in the form.
        labels (dict): A dictionary of labels for each field.
        widgets (dict): A dictionary of widgets for each field.
    """

    class Meta:
        model = House
        fields = [
            'house_number', 'address', 'country', 'state', 'city', 'house_size', 
            'number_of_apartments', 'number_of_floors', 'garage_space', 'yard_size', 
            'renovation_year', 'condition', 'features', 'utilities', 'sale_price', 
            'rent_price', 'occupancy_status', 'notes'
        ]

        labels = {
            'house_number': 'House Number',
            'address': 'Address',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'house_size': 'House Size (square metres)',
            'number_of_apartments': 'Number of Apartments',
            'number_of_floors': 'Total Floor Number',
            'garage_space': 'Garage Space',
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
            'house_number': forms.NumberInput(attrs={
                'placeholder': 'Enter House Number',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter address',
                'cols': 45,
                'rows': 8,
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Enter city',
            }),
            'country': forms.Select(attrs={
                'id': 'id_country',
            }),
            'state': forms.Select,
            'utilities': forms.SelectMultiple,
            'features': forms.SelectMultiple,
            'renovation_year': forms.NumberInput(attrs={
                'placeholder': 'Enter renovation year',
                'value': 1900,
            }),
            'occupancy_status': forms.Select(choices=House.OCCUPANCY),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Enter notes',
                'cols': 45,
                'rows': 8,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(HouseForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_house_number(self):
        house_number = self.cleaned_data.get('house_number')

        if house_number <= 0:
            messages.error(self.request, "House number must be greater than zero.")
            raise ValidationError('House number must be greater than zero.')
        
        return house_number
    
    def clean_renovation_year(self):
        renovation_year = self.cleaned_data.get('renovation_year')

        if renovation_year.isdigit():
            if int(renovation_year) < 1900 or int(renovation_year) > 2100:
                messages.error(self.request, "Enter a valid renovation year between 1900 and 2100")
                raise ValidationError("Enter a valid renovation year.")

        return renovation_year
     