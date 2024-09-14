import datetime
from django import forms
from django.forms import ModelForm
from .models import Estate
from django.contrib import messages


class EstateForm(ModelForm):
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
        fields = ['estate_name', 'address' , 'country', 'state', 'city', 'estate_type', 'year_built', 'number_of_houses', 'total_area_covered', 'land_area',
                  'estate_parking_spaces', 'construction_type','amenities', 'security_features', 'maintenance_cost',
                  'utilities', 'description',]
        widgets = {
            'year_built': forms.NumberInput(attrs={'value': 1900}),
            'amenities': forms.SelectMultiple,
            'security_features':forms.SelectMultiple,
            'utilities': forms.SelectMultiple,
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'estate_type': forms.Select(choices=Estate.DESIGNATION),
            'construction_type': forms.Select(choices=Estate.CONSTRUCTION_TYPES)
        }
        labels = {
            'total_area_covered': 'Total Area Covered (acres)',
            'land_area': 'Land Area (square metres)',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EstateForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})

country_choice = [('', 'Select a Country')]
for country in Estate.objects.values_list('country_id__name', flat=True):
    choice = (country, country)
    if choice not in country_choice and choice != (None, None):
        country_choice.append(choice)

state_choice = [('', 'Select a State')]
for state in Estate.objects.values_list('state_id__name', flat=True):
    choice = (state, state)
    if choice not in state_choice and choice != (None, None):
        state_choice.append(choice)

class EstateFilterForm(forms.ModelForm):
    estate_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False)
    _country = forms.ChoiceField(choices=sorted(country_choice), label="Country", required=False)
    _state = forms.ChoiceField(choices=sorted(state_choice), label="State", required=False)

    class Meta:
        model = Estate
        fields = ['estate_name', 'address', '_country', '_state', 'city',
        'construction_type',  'number_of_houses','maintenance_cost', 'total_area_covered',
        'utilities', 'security_features', 'amenities'
        ]

        widgets = {
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter address',
                'cols': 45,
                'rows': 2,
                'class': 'form-control'
            }),
        }

        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            super(EstateFilterForm, self).__init__(*args, **kwargs)
            self.fields['number_of_houses'].value = ""
            self.fields['total_area_covered'].initial = ""
            self.fields['maintenance_cost'].initial = ""

            # Define placeholders for each field
            placeholders = {
                'estate_name': 'Enter Estate Name',
                'address': 'Enter address',
                '_country': 'Select country',
                '_state': 'Select state',
                'city': 'Enter city',
                'construction_type': 'Select Contruction Type',
                'number_of_houses': 'Enter Number of Houses',
                'maintenance_cost': 'Enter maintenance cost',
                'utilities': 'Select Utilities',
                'amenities': 'Select Amenities',
                'security_features': 'Select Security features',
            }

            # Apply 'form-control' class and placeholders to all fields
            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'form-control'})

                if name in placeholders:
                    field.widget.attrs.update({'placeholder': placeholders[name]})

                # Set the 'min' attribute to 0 for all decimal and integer fields
                if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                    field.widget.attrs.update({'min': '0'})
            