from django.forms import ModelForm
from django.core.validators import RegexValidator
from django import forms
from .models import Company


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'number', 'email', 'website', 'cac', 'logo', 'year_founded']

        help_texts = {
            'website': ' (Optional)',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Enter Company Name"}),
            'website': forms.URLInput(attrs={'placeholder': 'https://www.example.com'}),
            'address': forms.TextInput(attrs={'placeholder': "Enter Company's Address", }),
            'logo': forms.FileInput,
            'number': forms.TextInput(attrs={'placeholder': "Enter Company's Number"}),
            'year_founded': forms.NumberInput(attrs={'value': '1900'}),
            'email': forms.TextInput(attrs={'placeholder': "Enter Company's Email"}),
            'cac': forms.TextInput(attrs={'placeholder': "Enter Company's CAC"}),
        }

        labels = {
            'name': 'Company Name',
            'address': 'Company Address',
            'email': 'Company Email',
            "number": 'Company Number',
            'website': 'Company Website',
            'logo': 'Company Logo',
            'cac': 'Company CAC ',
        }
