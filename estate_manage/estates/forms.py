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
    AMENITIES = [
        ('parking', 'Parking'),
        ('gym', 'Gym'),
        ('swimming_pool', 'Swimming pool'),
        ('cafeteria', 'Cafeteria'),
        ('spa', 'Spa'),
        ('playground', 'Playground'),
        ('terraces', 'Terraces'),
        ('helipads', 'Helipads'),
        ('package_locker', 'Package locker'),
        ('pet_friendly_amenities', 'Pet-Friendly Amenities'),
        ('laundry_facilities', 'Laundry facilities'),
    ]

    SECURITY = [
        ('perimeter_security', 'Perimeter Security'),
        ('access_control_systems', 'Access Control Systems'),
        ('surveillance_technology', 'Surveillance Technology'),
        ('interior_security_measures', 'Interior Security Measures',),
        ('balancing_visibility_and_discretion', 'Balancing Visibility and Discretion'),
        ('regular_audits_and_assessments', 'Regular Audits and Assessments'),
    ]

    UTILITIES = [
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
        ('sewage', 'Sewage'),
        ('security', 'Security'),
        ('elevator', 'Elevator'),
        ('trash_collection', 'Trash Collection'),
        ('garbage_collection', 'Garbage Collection'),
    ]

    _images = MultipleFileField(label='Estate Images', required=False)
    _amenity = forms.MultipleChoiceField(choices=AMENITIES, widget=forms.CheckboxSelectMultiple,
                                         label='Amenities')
    _security = forms.MultipleChoiceField(choices=SECURITY, widget=forms.CheckboxSelectMultiple,
                                          label='Security Features')
    _utility = forms.MultipleChoiceField(choices=UTILITIES, widget=forms.CheckboxSelectMultiple,
                                         label='Utilities')

    class Meta:
        model = Profile
        fields = ['estate_name', 'estate_location', 'estate_type', '_images', 'year_built', 'number_of_houses',
                  'number_of_apartments', 'total_area_covered', 'land_area', 'total_floor_number',
                  'estate_parking_spaces', '_amenity', 'construction_type', 'maintenance_cost', '_security', '_utility',
                  'current_occupancy', 'vacancy_rate', 'estate_description']
        widgets = {
            'year_built': forms.NumberInput(attrs={'value': 1900})
        }
        labels = {
            'total_area_covered': 'Total Area Covered (acres)',
            'land_area': 'Land Area (square metres)',
        }

    # clean methods
    def clean__amenity(self):
        # Cleans the '_amenity' field data, joins the list of amenities into a single string separated by commas.
        return ','.join(self.cleaned_data['_amenity'])

    def clean__security(self):
        # Cleans the '_security' field data, joins the list of security features into a single string separated by
        # commas.
        return ','.join(self.cleaned_data['_security'])

    def clean__utility(self):
        # Cleans the '_utility' field data, joins the list of utilities into a single string separated by commas.
        return ','.join(self.cleaned_data['_utility'])

    # save method
    def save(self, commit=True):
        # Create a model instance without saving it to the database yet.
        instance = super(ProfileForm, self).save(commit=False)

        # Set the 'amenities' field of the instance with the cleaned '_amenity' data.
        instance.amenities = self.cleaned_data['_amenity']

        # Set the 'security_features' field of the instance with the cleaned '_security' data.
        instance.security_features = self.cleaned_data['_security']

        # Set the 'utility' field of the instance with the cleaned '_utility' data.
        instance.utility = self.cleaned_data['_utility']

        # If the commit is True, save the instance to the database.
        if commit:
            instance.save()

        # Return the model instance.
        return instance
