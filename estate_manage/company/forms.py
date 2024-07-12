from django import forms
from django.forms import ModelForm
from .models import *

class CompanyForm(ModelForm):
    class meta:
        model = Company
        fields = ['com_name', 'com_address', 'com_number', 'com_mail', 'com_web', 'com_cac',
                   'com_logo', 'com_year_founded']
        
        labels = {
            'com_name': 'Company Name', 
            'com_address': 'Company address',
            'com_number': 'Company number',
            'com_mail': 'company Email',
            'com_web': 'Company website',
            'com_cac' : 'Company CAC',
            'com_logo': 'Company logo',
            'com_year_founded': 'Year founded'
                 # Custom label for all field
        }

        help_texts = {
            'com_web':  ' (Optional)', 
        }