from django.forms import ModelForm
from .models import *


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'number', 'email', 'website', 'cac', 'logo', 'year_founded']

        help_texts = {
            'website': ' (Optional)',
        }
