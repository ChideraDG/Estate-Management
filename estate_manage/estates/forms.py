from django import forms
from django.forms import ModelForm
from .models import Profile


class MultipleFileInput(forms.ClearableFileInput):
    # This class inherits from forms.ClearableFileInput and allows for multiple file selection.
    allow_multiple_selected = True  # Enables the HTML input element to accept multiple files.


class MultipleFileField(forms.FileField):
    # This class inherits from forms.FileField and uses MultipleFileInput as its widget.
    def __init__(self, *args, **kwargs):
        # Sets the widget to MultipleFileInput which allows multiple file selection.
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)  # Calls the parent constructor with the modified kwargs.

    def clean(self, data, initial=None):
        # This method cleans the input data. If multiple files are uploaded, it cleans each one.
        single_file_clean = super().clean  # Reference to the parent class's clean method.
        if isinstance(data, (list, tuple)):  # Checks if data is a list or tuple (i.e., multiple files).
            result = [single_file_clean(d, initial) for d in data]  # Cleans each file in the list.
        else:
            result = single_file_clean(data, initial)  # Cleans a single file.
        return result  # Returns the cleaned data.


class ProfileForm(ModelForm):
    _images = MultipleFileField(label='Estate Images', required=False)

    class Meta:
        model = Profile
        fields = ['estate_name', 'estate_location', 'estate_type', '_images', 'year_built', 'number_of_houses',
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
