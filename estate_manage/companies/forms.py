from django.forms import ModelForm
from django.core.validators import RegexValidator
from django import forms
from .models import Company


class CompanyForm(ModelForm):
    number_regex = RegexValidator(
        regex=r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
        message="Phone number must be entered in the format: '08012345678' or '+2348012345678'. Up to 15 digits "
                "allowed."
    )
    phone_number = forms.CharField(
        validators=[number_regex],
        widget=forms.TextInput(attrs={'placeholder': "Enter Company's Number"}),
        label='Company Number'
    )

    class Meta:
        model = Company
        fields = ['name', 'address', 'phone_number', 'email', 'website', 'cac', 'logo', 'year_founded']

        help_texts = {
            'website': ' (Optional)',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Enter Company Name"}),
            'website': forms.URLInput(attrs={'placeholder': 'https://www.example.com'}),
            'address': forms.TextInput(attrs={'placeholder': "Enter Company's Address", }),
            'logo': forms.FileInput,
            'year_founded': forms.NumberInput(attrs={'value': '1900'}),
            'email': forms.TextInput(attrs={'placeholder': "Enter Company's Email"}),
            'cac': forms.TextInput(attrs={'placeholder': "Enter Company's CAC"}),
        }

        labels = {
            'name': 'Company Name',
            'address': 'Company Address',
            'email': 'Company Email',
            'website': 'Company Website',
            'logo': 'Company Logo',
            'cac': 'Company CAC ',
        }
