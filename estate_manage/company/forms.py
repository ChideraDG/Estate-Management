from django.forms import ModelForm
from .models import *


class CompanyForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'address', 'number', 'email', 'website', 'cac', 'logo', 'year_founded']

        help_texts = {
            'web': ' (Optional)',
        }
