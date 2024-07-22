from django import forms
from django.forms import ModelForm
from .models import Estate


class ProfileForm(ModelForm):

    class Meta:
        model = Estate
        fields = ['estate_name', 'estate_location', 'estate_type', 'year_built', 'number_of_houses',
                  'number_of_apartments', 'total_area_covered', 'land_area', 'total_floor_number',
                  'estate_parking_spaces', 'amenities', 'construction_type', 'maintenance_cost', 'security_features',
                  'utilities', 'current_occupancy', 'vacancy_rate', 'estate_description']
        widgets = {
            'year_built': forms.NumberInput(attrs={'value': 1900}),
            'amenities': forms.CheckboxSelectMultiple,
            'security_features': forms.CheckboxSelectMultiple,
            'utilities': forms.CheckboxSelectMultiple,
        }
        labels = {
            'total_area_covered': 'Total Area Covered (acres)',
            'land_area': 'Land Area (square metres)',
        }
