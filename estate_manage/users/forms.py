import datetime
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from .models import Profile


class RegistrationForm(forms.Form):
    """
    A form for user registration.

    Attributes:
        username (str): The username of the user.
        full_name (str): The full name of the user.
        email (str): The email address of the user.
        designation (str): The designation of the user.
        password1 (str): The password of the user.
        password2 (str): The confirmation password of the user.

    Example:
        >>> form = RegistrationForm({
        ...     'username': 'john_doe',
        ...     'full_name': 'John Doe',
        ...     'email': 'john@example.com',
        ...     'designation': 'buyer',
        ...     'password1': 'password123',
        ...     'password2': 'password123'
        ... })
        >>> form.is_valid()
        True
    """

    validation_error = None

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

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            self.validation_error = 'Username already exists'
            raise forms.ValidationError('')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.validation_error = 'Email already exists'
            raise forms.ValidationError("")
        return email
    
    def clean_password2(self):
        """
        Validate that the two password fields match.

        Raises:
            forms.ValidationError: If the two password fields do not match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.validation_error = 'Passwords do not match'
            raise forms.ValidationError("Passwords do not match")

        return password2
    
    def get_error(self):
        return self.validation_error


class LoginForm(forms.Form):
    """
    A form for user login.

    Attributes:
        username_or_email (str): The username or email address of the user.
        password (str): The password of the user.

    Example:
        >>> form = LoginForm({
        ...     'username_or_email': 'john_doe',
        ...     'password': 'password123'
        ... })
        >>> form.is_valid()
        True
    """

    username_or_email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CustomPasswordResetForm(PasswordResetForm):
    """
    A custom form for password reset.

    Attributes:
        email (str): The email address of the user.

    Example:
        >>> form = CustomPasswordResetForm({
        ...     'email': 'john@example.com'
        ... })
        >>> form.is_valid()
        True
    """

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    A custom form for setting a new password.

    Attributes:
        new_password1 (str): The new password of the user.
        new_password2 (str): The confirmation of the new password.

    Example:
        >>> form = CustomSetPasswordForm({
        ...     'new_password1': 'new_password123',
        ...     'new_password2': 'new_password123'
        ... })
        >>> form.is_valid()
        True
    """

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
    """
    A form for handling general contact inquiries.

    Attributes:
        name (CharField): The name of the person submitting the form.
        email (EmailField): The email address of the person submitting the form.
        subject (CharField): The subject of the contact inquiry.
        message (CharField): The message being sent.

    Example:
        >>> from django import forms
        >>> form = ContactForm({
        ...     'name': 'John Doe',
        ...     'email': 'john@example.com',
        ...     'subject': 'Test Subject',
        ...     'message': 'This is a test message.'
        ... })
        >>> form.is_valid()
        True
    """
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


class ContactAgentForm(forms.Form):
    """
    A form for handling contact inquiries specifically for agents.

    Attributes:
        name (CharField): The name of the person submitting the form.
        email (EmailField): The email address of the person submitting the form.
        message (CharField): The message being sent.

    Example:
        >>> from django import forms
        >>> form = ContactAgentForm({
        ...     'name': 'Jane Doe',
        ...     'email': 'jane@example.com',
        ...     'message': 'This is a test message for an agent.'
        ... })
        >>> form.is_valid()
        True
    """
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

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ("user", "designation", "created", "updated")

        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date', 
                                                           'min': str(datetime.datetime(year=1900, month=1, day=1).date()),
                                                           'max': str(datetime.datetime(year=2014, month=1, day=1).date())}),
                    'phone_number': forms.TextInput(attrs={'placeholder': "Enter your Phone Number"})}