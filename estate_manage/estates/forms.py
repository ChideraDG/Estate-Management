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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EstateForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            # Set the 'min' attribute to 0 for all decimal and integer fields
            if isinstance(field, (forms.DecimalField, forms.IntegerField)):
                field.widget.attrs.update({'min': '0'})

# country_choice = [('', 'Select a Country')]
# for country in Estate.objects.values_list('country_id__name', flat=True):
#     choice = (country, country)
#     if choice not in country_choice and choice != (None, None):
#         country_choice.append(choice)

# state_choice = [('', 'Select a State')]
# for state in Estate.objects.values_list('state_id__name', flat=True):
#     choice = (state, state)
#     if choice not in state_choice and choice != (None, None):
#         state_choice.append(choice)

class EstateFilterForm(forms.ModelForm):
    pass
    # name = forms.CharField(required=False)
    # address = forms.CharField(required=False)
    # estate_type = forms.CharField(required=False)
    # construction_type = forms.CharField(required=False)
    # _country = forms.ChoiceField(choices=sorted(country_choice), label="Country", required=False)
    # _state = forms.ChoiceField(choices=sorted(state_choice), label="State", required=False)
        