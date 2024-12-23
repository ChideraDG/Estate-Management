import datetime
from django.forms import ModelForm
from django import forms
from django.contrib import messages
from .models import House
from agents.models import Agent
from locations.models import Country, State


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

    _agent = forms.ModelChoiceField(queryset=Agent.objects.all(), empty_label="Select an Agent (if needed)", required=False)
    class Meta:
        model = House
        fields = [
            'house_number', '_agent', 'address', 'country', 'state', 'city', 'house_size',
            'number_of_floors', 'garage_space', 'yard_size', 
            'renovation_year', 'condition', 'features', 'utilities', 'sale_price', 
            'rent_price', 'notes'
        ]

        labels = {
            'house_number': 'House Number',
            '_agent': 'Agent',
            'address': 'Address',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'house_size': 'House Size (square metres)',
            'number_of_floors': 'Total Floor Number',
            'garage_space': 'Garage Space',
            'yard_size': 'Yard Size (square metres)',
            'renovation_year': 'Renovation Year',
            'condition': 'Condition',
            'features': 'Features',
            'utilities': 'Utilities',
            'sale_price': 'Sale Price',
            'rent_price': 'Rent Price',
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
                'min': '1900',
                'max': f'{datetime.datetime.now().year}',
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Enter notes',
                'cols': 45,
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.estate = kwargs.pop('estate', None)  # Get the estate from kwargs
        super(HouseForm, self).__init__(*args, **kwargs)
        
        # Prepopulate the 'country' field based on the estate
        if self.estate and hasattr(self.estate, 'country'):
            self.fields['country'].initial = self.estate.country
            self.fields['country'].disabled = True
        
        # Prepopulate the 'state' field based on the estate
        if self.estate and hasattr(self.estate, 'state'):
            self.fields['state'].initial = self.estate.state
            self.fields['state'].disabled = True

        # Prepopulate the 'address' field based on the estate
        if self.estate and hasattr(self.estate, 'address'):
            self.fields['address'].initial = self.estate.address
            self.fields['address'].disabled = True
            
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})

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
            'renovation_year', 'features', 'utilities'
        ]
        widgets = {
            'house_address': forms.Textarea(attrs={
                'placeholder': 'Enter address',
                'cols': 45,
                'rows': 2,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(HouseFilterForm, self).__init__(*args, **kwargs)
        self.fields['number_of_apartments'].initial = ""
        self.fields['number_of_floors'].initial = ""
        self.fields['garage_space'].initial = ""

        # Define placeholders for each field
        placeholders = {
            'house_no': 'Enter house number',
            'house_address': 'Enter address',
            '_country': 'Select country',
            '_state': 'Select state',
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

        # Filter countries and states based on user's previously added houses
        if self.request:
            company = self.request.user.profile.companies
            user_houses = House.objects.filter(company=company)
            user_countries = Country.objects.filter(houses__in=user_houses).distinct()
            user_states = State.objects.filter(houses__in=user_houses).distinct()

            # Set the choices for _country and _state
            self.fields['_country'].choices = [('', 'Select Country')] + [(country.name, country.name) for country in user_countries]
            self.fields['_state'].choices = [('', 'Select State')] + [(state.name, state.name) for state in user_states]

    def clean(self):
        cleaned_data = super().clean()

        # Retrieve form fields
        house_size_min = cleaned_data.get("house_size_min")
        house_size_max = cleaned_data.get("house_size_max")
        sale_price_min = cleaned_data.get("sale_price_min")
        sale_price_max = cleaned_data.get("sale_price_max")
        rent_price_min = cleaned_data.get("rent_price_min")
        rent_price_max = cleaned_data.get("rent_price_max")
        yard_size_min = cleaned_data.get("yard_size_min")
        yard_size_max = cleaned_data.get("yard_size_max")

        # Validate that minimum values are not greater than maximum values
        if house_size_min and house_size_max and house_size_min > house_size_max:
            messages.error(self.request, "Min House Size cannot be greater than Max House Size.")
            self.add_error("house_size_min", "Min House Size cannot be greater than Max House Size.")
        
        if sale_price_min and sale_price_max and sale_price_min > sale_price_max:
            messages.error(self.request, "Min Sale Price cannot be greater than Max Sale Price.")
            self.add_error("sale_price_min", "Min Sale Price cannot be greater than Max Sale Price.")
        
        if rent_price_min and rent_price_max and rent_price_min > rent_price_max:
            messages.error(self.request, "Min Rent Price cannot be greater than Max Rent Price.")
            self.add_error("rent_price_min", "Min Rent Price cannot be greater than Max Rent Price.")
        
        if yard_size_min and yard_size_max and yard_size_min > yard_size_max:
            messages.error(self.request, "Min Yard Size cannot be greater than Max Yard Size.")
            self.add_error("yard_size_min", "Min Yard Size cannot be greater than Max Yard Size.")

        return cleaned_data
    