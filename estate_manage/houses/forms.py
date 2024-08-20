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
                'rows': 4,
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
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(HouseForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})

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

country_choice = [('', 'Select a Country')]
for country in House.objects.values_list('country_id__name', flat=True):
    choice = (country, country)
    if choice not in country_choice and choice != (None, None):
        country_choice.append(choice)

state_choice = [('', 'Select a State')]
for state in House.objects.values_list('state_id__name', flat=True):
    choice = (state, state)
    if choice not in state_choice and choice != (None, None):
        state_choice.append(choice)
    
class HouseFilterForm(forms.ModelForm):
    house_no = forms.IntegerField(required=False, label="House number")
    house_address = forms.CharField(required=False)
    house_size_min = forms.DecimalField(required=False)
    house_size_max = forms.DecimalField(required=False)
    sale_price_min = forms.DecimalField(required=False)
    sale_price_max = forms.DecimalField(required=False)
    rent_price_min = forms.DecimalField(required=False)
    rent_price_max = forms.DecimalField(required=False)
    yard_size_min = forms.IntegerField(required=False)
    yard_size_max = forms.IntegerField(required=False)
    _country = forms.ChoiceField(choices=sorted(country_choice), label="Country", required=False)
    _state = forms.ChoiceField(choices=sorted(state_choice), label="State", required=False)

    class Meta:
        model = House
        fields = [
            'house_no', 'house_address', '_country', '_state', 'city',
            'number_of_apartments', 'number_of_floors', 'garage_space',
            'renovation_year', 'condition', 'features', 'utilities'
        ]
        widgets = {
            'house_address': forms.Textarea(attrs={
                'placeholder': 'Enter address',
                'cols': 45,
                'rows': 2,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(HouseFilterForm, self).__init__(*args, **kwargs)

        # Define placeholders for each field
        placeholders = {
            'house_no': 'Enter house number',
            'house_address': 'Enter address',
            '_country': 'Select country',
            'state': 'Select state',
            'city': 'Enter city',
            'house_size_min': 'Min house size',
            'house_size_max': 'Max house size',
            'sale_price_min': 'Min sale price',
            'sale_price_max': 'Max sale price',
            'rent_price_min': 'Min rent price',
            'rent_price_max': 'Max rent price',
            'number_of_apartments': 'Enter number of apartments',
            'number_of_floors': 'Enter number of floors',
            'garage_space': 'Enter garage space',
            'yard_size_min': 'Min yard size',
            'yard_size_max': 'Max yard size',
            'renovation_year': 'Enter renovation year',
            'condition': 'Select condition',
            'features': 'Select features',
            'utilities': 'Select utilities',
        }

        # Apply 'form-control' class and placeholders to all fields
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[name]})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})
