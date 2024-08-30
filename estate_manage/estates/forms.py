from django import forms
from django.forms import ModelForm
from .models import Estate


class ProfileForm(ModelForm):
    """
    A form for creating or editing an Estate profile.

    The form includes fields for estate name, location, type, year built, and more.
    It uses various widgets to enhance the user experience, such as checkbox select
    multiple for amenities, security features, and utilities.

    Attributes:
        model (Estate): The model that this form is based on.
        fields (list): A list of fields to include in the form.
        widgets (dict): A dictionary of widgets to use for each field.
        labels (dict): A dictionary of custom labels for each field.
    """

    class Meta:
        model = Estate
        fields = ['name', 'address', 'estate_type', 'year_built', 'number_of_houses', 'total_area_covered', 'land_area',
                  'estate_parking_spaces', 'amenities', 'construction_type', 'maintenance_cost', 'security_features',
                  'utilities', 'description', 'country', 'state', 'city']
        widgets = {
            'year_built': forms.NumberInput(attrs={'value': 1900}),
            'amenities': forms.CheckboxSelectMultiple(),
            'security_features': forms.CheckboxSelectMultiple(),
            'utilities': forms.CheckboxSelectMultiple(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'estate_type': forms.Select(choices=Estate.DESIGNATION),
            'construction_type': forms.Select(choices=Estate.CONSTRUCTION_TYPES)
        }
        labels = {
            'total_area_covered': 'Total Area Covered (acres)',
            'land_area': 'Land Area (square metres)',
        }
        