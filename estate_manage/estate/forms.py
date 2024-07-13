import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class RegistrationForm(ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        elif re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$. #!%*?&])[A-Za-z\d@$!#% *?.&]{8,}$", password1):
            raise forms.ValidationError("Passwords are not the same")

        return password2

    class Meta:
        model = Registration
        fields = ['full_name', 'gender', 'date_of_birth', 'email', 'phone_number', 'designation', 'state_of_origin',
                  'state_of_residence', 'city', 'address_1', 'address_2', 'password1', 'password2']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'full_name': 'Full Name',  # Custom label for the fullname field
        }
        help_texts = {
            'address_2': ' (Optional)',  # Help text for the phone number field
        }


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your Email Here'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': "•••••••••••"}))
