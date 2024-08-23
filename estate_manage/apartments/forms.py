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
            'is_occupied',
            'last_renovation_year', 
            'condition', 
            'notes',
        ]
        
        widgets = {
            'apartment_number': forms.TextInput(attrs={'placeholder': 'Enter apartment number'}),
            'floor_number': forms.NumberInput(attrs={'placeholder': 'Enter floor number'}),
            'number_of_rooms': forms.NumberInput(attrs={'placeholder': 'Enter number of rooms'}),
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
            'is_occupied': forms.NullBooleanSelect,
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
        
        # Check if the apartment number already exists
        if Apartment.objects.filter(apartment_number=apartment_number).exists():
            messages.error(self.request, "This apartment number is already in use. Please choose a unique apartment number.")
            raise forms.ValidationError("This apartment number is already in use. Please choose a unique apartment number.")
        
        return apartment_number
