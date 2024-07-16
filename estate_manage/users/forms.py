import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class RegistrationForm(forms.Form):
    DESIGNATION = [
        ('company', 'Company'),
        ('tenant', 'Tenant'),
        ('land_owner', 'Land Owner'),
        ('agent', 'Agent'),
    ]

    username = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'id': 'name', 'placeholder': 'Enter your Username Here'}))
    full_name = forms.CharField(max_length=100, required=True,
                                widget=forms.TextInput(attrs={'id': 'name', 'placeholder': 'Enter your Full Name Here'}))
    email = forms.EmailField(max_length=100, required=True,
                             widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Enter your Email Here'}))
    designation = forms.ChoiceField(choices=DESIGNATION)
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': "••••••••"}))
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': "••••••••"}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        # elif re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$. #!%*?&])[A-Za-z\d@$!#% *?.&]{8,}$", password1):
        #     raise forms.ValidationError("Password strength is weak")

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
