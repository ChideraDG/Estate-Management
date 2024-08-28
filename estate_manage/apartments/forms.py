import datetime
from django.contrib import messages
from django import forms
from .models import Apartment


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'apartment_number', 
            'floor_number', 
            'number_of_rooms', 
            'size_in_sqft', 
            'balcony', 
            'parking_space', 
            'is_furnished', 
            'number_of_bathrooms', 
            'number_of_bedrooms', 
            'kitchen_type', 
            'flooring_type', 
            'heating_system', 
            'air_conditioning', 
            'water_supply', 
            'electricity_supply', 
            'internet_ready', 
            'cable_tv_ready', 
            'rent_price', 
            'sale_price', 
            'security_deposit', 
            'maintenance_fee',
            'last_renovation_year', 
            'condition', 
            'notes',
        ]
        
        widgets = {
            'apartment_number': forms.TextInput(attrs={'placeholder': 'Enter apartment number', 'min': '1',}),
            'floor_number': forms.NumberInput(attrs={'placeholder': 'Enter floor number', 'min': '1',}),
            'number_of_rooms': forms.NumberInput(attrs={'placeholder': 'Enter number of rooms', 'min': '1'}),
            'size_in_sqft': forms.NumberInput(attrs={'placeholder': 'Enter apartment size in square feet'}),
            'balcony': forms.NullBooleanSelect,
            'parking_space': forms.NullBooleanSelect,
            'is_furnished': forms.NullBooleanSelect,
            'number_of_bathrooms': forms.NumberInput(attrs={'placeholder': 'Enter number of bathrooms'}),
            'number_of_bedrooms': forms.NumberInput(attrs={'placeholder': 'Enter number of bedrooms'}),
            'kitchen_type': forms.Select(attrs={'placeholder': 'Select kitchen type'}),
            'flooring_type': forms.Select(attrs={'placeholder': 'Select flooring type'}),
            'heating_system': forms.Select(attrs={'placeholder': 'Select heating system'}),
            'air_conditioning': forms.NullBooleanSelect,
            'water_supply': forms.Select(attrs={'placeholder': 'Select water supply type'}),
            'electricity_supply': forms.Select(attrs={'placeholder': 'Select electricity supply type'}),
            'internet_ready': forms.NullBooleanSelect,
            'cable_tv_ready': forms.NullBooleanSelect,
            'rent_price': forms.NumberInput(attrs={'placeholder': 'Enter rent price'}),
            'sale_price': forms.NumberInput(attrs={'placeholder': 'Enter sale price (if applicable)'}),
            'security_deposit': forms.NumberInput(attrs={'placeholder': 'Enter security deposit amount'}),
            'maintenance_fee': forms.NumberInput(attrs={'placeholder': 'Enter maintenance fee (if applicable)'}),
            'last_renovation_year': forms.NumberInput(attrs={
                'placeholder': 'Enter last renovation year',
                'value': 1900,
                'min': '1900',
                'max': f'{datetime.datetime.now().year}',
            }),
            'condition': forms.Select(attrs={'placeholder': 'Select apartment condition'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter any additional notes'}),
        }

        labels= {
            'apartment_number': 'Apartment Number',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ApartmentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})
    
    def clean_apartment_number(self):
        apartment_number = self.cleaned_data.get('apartment_number')
        house = self.cleaned_data.get('house')

        # Check if another apartment with the same number exists in the same house
        if Apartment.objects.filter(house=house, apartment_number=apartment_number).exists():
            messages.error(self.request, f"Apartment {apartment_number} already exists in this house.")
            raise forms.ValidationError(f"Apartment {apartment_number} already exists in this house.")
        
        return apartment_number
    

class ApartmentFilterForm(forms.Form):
    from django import forms

class ApartmentFilterForm(forms.Form):
    apartment_number = forms.CharField(
        required=False,
        label="Apartment Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Apartment Number'})
    )
    floor_number = forms.IntegerField(
        required=False,
        label="Floor Number",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Floor Number'})
    )
    number_of_bedrooms = forms.IntegerField(
        required=False,
        label="Number of Bedrooms",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Number of Bedrooms'})
    )
    number_of_bathrooms = forms.IntegerField(
        required=False,
        label="Number of Bathrooms",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Number of Bathrooms'})
    )
    square_feet_min = forms.IntegerField(
        required=False,
        label="Min Square Feet",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Min Square Feet'})
    )
    square_feet_max = forms.IntegerField(
        required=False,
        label="Max Square Feet",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Max Square Feet'})
    )
    rent_price_min = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Min Rent Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Min Rent Price'})
    )
    rent_price_max = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Max Rent Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Max Rent Price'})
    )
    sale_price_min = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Min Sale Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Min Sale Price'})
    )
    sale_price_max = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Max Sale Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Max Sale Price'})
    )
    number_of_rooms = forms.IntegerField(
        required=False,
        label="Number of Rooms",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Number of Rooms'})
    )
    kitchen_type = forms.ChoiceField(
        required=False,
        choices=[('', '--------'), ('Open', 'Open'), ('Closed', 'Closed')],
        label="Kitchen Type",
        widget=forms.Select(attrs={'placeholder': 'Select Kitchen Type'})
    )
    flooring_type = forms.ChoiceField(
        required=False,
        choices=[('', '--------'), ('Tile', 'Tile'), ('Wood', 'Wood'), ('Carpet', 'Carpet')],
        label="Flooring Type",
        widget=forms.Select(attrs={'placeholder': 'Select Flooring Type'})
    )
    heating_system = forms.ChoiceField(
        required=False,
        choices=[('', '--------'), ('Central', 'Central'), ('Electric', 'Electric'), ('Gas', 'Gas')],
        label="Heating System",
        widget=forms.Select(attrs={'placeholder': 'Select Heating System'})
    )
    security_deposit = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Security Deposit",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Security Deposit'})
    )
    maintenance_fee = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Maintenance Fee",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Maintenance Fee'})
    )
    last_renovation_year = forms.IntegerField(
        required=False,
        label="Last Renovation Year",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Last Renovation Year'})
    )
    condition = forms.CharField(
        required=False,
        label="Condition",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Condition'})
    )

    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that min values are not greater than max values
        square_feet_min = cleaned_data.get("square_feet_min")
        square_feet_max = cleaned_data.get("square_feet_max")
        rent_price_min = cleaned_data.get("rent_price_min")
        rent_price_max = cleaned_data.get("rent_price_max")
        sale_price_min = cleaned_data.get("sale_price_min")
        sale_price_max = cleaned_data.get("sale_price_max")

        if square_feet_min and square_feet_max and square_feet_min > square_feet_max:
            messages.error(self.request, "Min Square Feet cannot be greater than Max Square Feet.")
            self.add_error("square_feet_min", "Min Square Feet cannot be greater than Max Square Feet.")
        
        if rent_price_min and rent_price_max and rent_price_min > rent_price_max:
            messages.error(self.request, "Min Rent Price cannot be greater than Max Rent Price.")
            self.add_error("rent_price_min", "Min Rent Price cannot be greater than Max Rent Price.")
        
        if sale_price_min and sale_price_max and sale_price_min > sale_price_max:
            messages.error(self.request, "Min Sale Price cannot be greater than Max Sale Price.")
            self.add_error("sale_price_min", "Min Sale Price cannot be greater than Max Sale Price.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ApartmentFilterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})

