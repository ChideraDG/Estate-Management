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
        fields = ['estate_name', 'address' , 'country', 'state', 'city', 'estate_type', 'year_built', 'total_area_covered', 'land_area',
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
    #  This is the change
    country_choice = [
        ('', 'Select a Country'),
        *sorted([(country, country) for country in set(Estate.objects.values_list('country_id__name', flat=True)) if country])  # Comment this line during database recovery
    ]

    state_choice = [
        ('', 'Select a State'),
        *sorted([(state, state) for state in set(Estate.objects.values_list('state_id__name', flat=True)) if state])  # Comment this line during database recovery
    ]

    # ends here

    estate_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Estate Name'}))
    address = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address'})
            )
    _country = forms.ChoiceField(choices=country_choice, label="Country", required=False,
             widget=forms.Select(attrs={'class': 'form-control',})
             )
    _state = forms.ChoiceField(choices=state_choice, label="State", required=False, 
            widget=forms.Select(attrs={'class': 'form-control',})
            )

    # Filter by number of houses (min-max range)
    min_number_of_houses = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Number of Houses',
            'min': '0'
        })
    )
    max_number_of_houses = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Number of Houses',
            'min': '0'
        })
    )

      # Filter by total area covered (min-max range)
    min_total_area_covered = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Area Covered (sq. ft)',
            'min': '0'
        })
    )
    max_total_area_covered = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Area Covered (sq. ft)',
            'min': '0'
        })
    )
    
    # Filter by land area (min-max range)
    min_land_area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Land Area (sq. ft)',
            'min': '0'
        })
    )
    max_land_area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Land Area (sq. ft)',
            'min': '0'
        })
    )
    
    # Filter by maintenance cost (min-max range)
    min_maintenance_cost = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Maintenance Cost',
            'min': '0'
        })
    )
    max_maintenance_cost = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Maintenance Cost',
            'min': '0'
        })
    )

    class Meta:
        model = Estate
        fields = ['estate_name', 'address', '_country', '_state', 'city',
        'construction_type',  'utilities', 'security_features', 'amenities'
        ]

        widgets = {
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter address',
                'cols': 45,
                'rows': 2,
                'class': 'form-control'
            }),
        'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
        'construction_type': forms.Select(attrs={'class': 'form-control'}),
        'utilities': forms.SelectMultiple(attrs={'class': 'form-control'}), 
        'security_features': forms.SelectMultiple(attrs={'class': 'form-control'}),
        'amenities': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EstateFilterForm, self).__init__(*args, **kwargs)
        self.fields['construction_type'].initial = ""

    def clean(self):
        cleaned_data = super().clean()

        # Retrieve form fields
        min_number_of_houses = cleaned_data.get("min_number_of_houses")
        max_number_of_houses = cleaned_data.get("max_number_of_houses")
        min_total_area_covered = cleaned_data.get("min_total_area_covered")
        max_total_area_covered = cleaned_data.get("max_total_area_covered")
        min_land_area = cleaned_data.get("min_land_area")
        max_land_area = cleaned_data.get("max_land_area")
        min_maintenance_cost = cleaned_data.get("min_maintenance_cost")
        max_maintenance_cost = cleaned_data.get("max_maintenance_cost")

        # Validate that minimum values are not greater than maximum values
        if min_number_of_houses is not None and max_number_of_houses is not None and min_number_of_houses > max_number_of_houses:
            self.add_error("min_number_of_houses", "Min Number of Houses cannot be greater than Max Number of Houses.")

        if min_total_area_covered is not None and max_total_area_covered is not None and min_total_area_covered > max_total_area_covered:
            self.add_error("min_total_area_covered", "Min Area Covered cannot be greater than Max Area Covered.")

        if min_land_area is not None and max_land_area is not None and min_land_area > max_land_area:
            self.add_error("min_land_area", "Min Land Area cannot be greater than Max Land Area.")

        if min_maintenance_cost is not None and max_maintenance_cost is not None and min_maintenance_cost > max_maintenance_cost:
            self.add_error("min_maintenance_cost", "Min Maintenance Cost cannot be greater than Max Maintenance Cost.")

        return cleaned_data
            