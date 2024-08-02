from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django import forms
from .models import *


class RegistrationForm(forms.Form):
    DESIGNATION = [
        ('', 'Select a Designation'),
        ('buyer', 'Buyer'),
        ('company', 'Company'),
        ('tenant', 'Tenant'),
        ('building_owner', 'Building Owner'),
        ('agent', 'Agent'),
    ]

    username = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'UserName'}))
    full_name = forms.CharField(max_length=100, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(max_length=100, required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    designation = forms.ChoiceField(choices=DESIGNATION, widget=forms.Select)
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2


class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm new password'
        })
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-a',
            'placeholder': 'Your Name',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg form-control-a',
            'placeholder': 'Your Email',
            'required': 'required'
        })
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-a',
            'placeholder': 'Subject',
            'required': 'required'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Message',
            'cols': 45,
            'rows': 8,
            'required': 'required'
        })
    )


class AgentMailForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg form-control-a',
            'placeholder': 'Name *',
            'required': 'required'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg form-control-a',
            'placeholder': 'Email *',
            'required': 'required'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Comment *',
            'cols': 45,
            'rows': 8,
            'required': 'required'
        })
    )

