from django.forms import ModelForm
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Tenant
from houses.models import House


class TenantForm(ModelForm):
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                message="Phone number must be entered in the format: '08012345678' or '+2348012345678'. Up to 15 digits allowed."
            )
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number', 'class': 'form-control'}),
        label='Phone Number')
        
    class Meta:
        model = Tenant
        fields = [
            'first_name', 'last_name', 'email', 'phone_number','country', 'state', 'city', 'profile_picture', 'move_in_date', 'lease_start_date',
            'lease_end_date', 'monthly_rent', 'deposit_amount', 'lease_term', 'payment_status', 'emergency_contact_name',
            'emergency_contact_number', 'employment_status', 'occupation'
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'profile_picture': 'Profile Picture',
            'move_in_date': 'Move In Date',
            'lease_start_date': 'Lease Start Date',
            'lease_end_date': 'Lease End Date',
            'monthly_rent': 'Monthly Rent',
            'deposit_amount': 'Deposit Amount',
            'lease_term': 'Lease Term',
            'payment_status': 'Payment Status',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_number': 'Emergency Contact Phone Number',
            'employment_status': 'Employment Status',
            'occupation': 'Occupation',
            'notes': 'Notes',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name',  'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name',  'class': 'form-control',}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email',  'class': 'form-control',}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number',  'class': 'form-control',}),
            'city': forms.TextInput(attrs={ 'placeholder': 'Enter city',  'class': 'form-control',}),
            'country': forms.Select(attrs={ 
                'placeholder': 'Select country',
                'class': 'form-control',
                'id': 'id_country',}),
            'state': forms.Select(attrs={
                 'placeholder': 'Select state',
                   'class': 'form-control',
                    'id': 'id_state',}),
            'profile_picture': forms.FileInput(attrs={ 'class': 'form-control',}),
            'move_in_date': forms.DateInput(attrs={'placeholder': 'Enter Move In Date', 'type': 'date',  'class': 'form-control',}),
            'lease_start_date': forms.DateInput(attrs={'placeholder': 'Enter Lease Start Date', 'type': 'date',  'class': 'form-control',}),
            'lease_end_date': forms.DateInput(attrs={'placeholder': 'Enter Lease End Date', 'type': 'date',  'class': 'form-control',}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Enter occupation',  'class': 'form-control',}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
            'lease_term': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'deposit_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_rent': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Name',  'class': 'form-control',}),
            'emergency_contact_number': forms.TextInput(attrs={'placeholder': 'Enter Emergency Contact Number',  'class': 'form-control',}),
            'notes': forms.Textarea(attrs={'placeholder': 'Enter note',
                                                        'cols': 45,
                                                        'rows': 8,
                                                        'class': 'form-control',
                                                        }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TenantForm, self).__init__(*args, **kwargs)

    def clean_contact_phone(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Example: Ensure the phone number is numeric and has 10 digits
        if not phone_number.replace("+", "").isdigit() or len(phone_number) <=10:
            messages.error(self.request, "Enter a valid Phone Number.")
            raise ValidationError('Enter a valid Phone number.')
        
        return phone_number


class AddTenantForm(forms.ModelForm):
    _house = forms.ModelChoiceField(queryset=House.objects.none(), 
                                    empty_label="Select a House",
                                    widget=forms.Select(attrs={'id': 'house_id'}))
    _apartment = forms.CharField(widget=forms.Select(attrs={'id': 'apartment_id'}))
    class Meta:
        model = Tenant
        fields = [ 
            '_house', '_apartment', 'first_name', 'last_name', 'email', 
            'phone_number', 'lease_start_date', 'lease_end_date', 
            'move_in_date', 'monthly_rent', 'deposit_amount', 
            'lease_term', 'payment_status', 'emergency_contact_name', 
            'emergency_contact_number', 'employment_status', 'occupation'
        ]

        # Optional: Add widgets or custom attributes for the form fields
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'move_in_date': forms.DateInput(attrs={'placeholder': 'Move-in Date', 'type': 'date'}),
            'lease_start_date': forms.DateInput(attrs={'placeholder': 'Lease Start Date', 'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'placeholder': 'Lease End Date', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'placeholder': 'Monthly Rent', 'min': '0.00'}),
            'deposit_amount': forms.NumberInput(attrs={'placeholder': 'Deposit Amount', 'min': '0.00'}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_number': forms.TextInput(attrs={'placeholder': 'Emergency Contact Number'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Occupation'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        building_owner = kwargs.pop('building_owner', None)
        super(AddTenantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Make all fields required
        for field in self.fields.values():
            if field.label == 'Emergency contact name' or field.label == 'Emergency contact number':
                field.required = False
            else:
                field.required = True

        # Filter the queryset based on the building_owner
        if building_owner:
            self.fields['_house'].queryset = House.objects.filter(building_owner=building_owner)
        else:
            self.fields['_house'].queryset = House.objects.none()


    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            messages.error(self.request, "Email address already exists")
            raise forms.ValidationError('Email address already exists')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        lease_start_date = cleaned_data.get("lease_start_date")
        lease_end_date = cleaned_data.get("lease_end_date")
        move_in_date = cleaned_data.get("move_in_date")

        # Check if lease start date is after lease end date
        if lease_start_date and lease_end_date and lease_start_date > lease_end_date:
            messages.error(self.request, "Lease start date cannot be after lease end date.")
            raise ValidationError("Lease start date cannot be after lease end date.")

        if move_in_date:
            if lease_end_date and move_in_date > lease_end_date:
                messages.error(self.request,"Move-in date cannot be after the lease end date.")
                raise ValidationError("Move-in date cannot be after the lease end date.")

        return cleaned_data


class TenantFilterForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label="First Name")
    last_name = forms.CharField(required=False, label="Last Name")
    email = forms.EmailField(required=False, label="Email")
    lease_start_date_min = forms.DateField(required=False, label="Lease Start Date (Min)", widget=forms.DateInput(attrs={'type': 'date'}))
    lease_start_date_max = forms.DateField(required=False, label="Lease Start Date (Max)", widget=forms.DateInput(attrs={'type': 'date'}))
    lease_end_date_min = forms.DateField(required=False, label="Lease End Date (Min)", widget=forms.DateInput(attrs={'type': 'date'}))
    lease_end_date_max = forms.DateField(required=False, label="Lease End Date (Max)", widget=forms.DateInput(attrs={'type': 'date'}))
    move_in_date_min = forms.DateField(required=False, label="Move-in Date (Min)", widget=forms.DateInput(attrs={'type': 'date'}))
    move_in_date_max = forms.DateField(required=False, label="Move-in Date (Max)", widget=forms.DateInput(attrs={'type': 'date'}))
    monthly_rent_min = forms.DecimalField(required=False, label="Min Monthly Rent")
    monthly_rent_max = forms.DecimalField(required=False, label="Max Monthly Rent")
    _house = forms.ModelChoiceField(queryset=House.objects.all(), required=False, label="House", empty_label="Select a House")

    class Meta:
        model = Tenant
        fields = [
            'first_name', 'last_name', 'email', '_house',
            'lease_start_date_min', 'lease_start_date_max', 'lease_end_date_min', 'lease_end_date_max',
            'move_in_date_min', 'move_in_date_max', 'monthly_rent_min', 'monthly_rent_max'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TenantFilterForm, self).__init__(*args, **kwargs)

        # Apply 'form-control' class and placeholders to all fields
        placeholders = {
            'first_name': 'Enter first name',
            'last_name': 'Enter last name',
            'email': 'Enter email address',
            '_house': 'Select a house',
            'lease_start_date_min': 'Min lease start date',
            'lease_start_date_max': 'Max lease start date',
            'lease_end_date_min': 'Min lease end date',
            'lease_end_date_max': 'Max lease end date',
            'move_in_date_min': 'Min move-in date',
            'move_in_date_max': 'Max move-in date',
            'monthly_rent_min': 'Min monthly rent',
            'monthly_rent_max': 'Max monthly rent',
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name in placeholders:
                field.widget.attrs.update({'placeholder': placeholders[name]})

            # Set the 'min' attribute to 0 for all decimal fields
            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({'min': '0'})

    def clean(self):
        cleaned_data = super().clean()

        # Validate that minimum values are not greater than maximum values
        if (cleaned_data.get("lease_start_date_min") and cleaned_data.get("lease_start_date_max") and
                cleaned_data["lease_start_date_min"] > cleaned_data["lease_start_date_max"]):
            messages.error(self.request, "Min Lease Start Date cannot be greater than Max Lease Start Date.")
            raise ValidationError("Min Lease Start Date cannot be greater than Max Lease Start Date.")

        if (cleaned_data.get("lease_end_date_min") and cleaned_data.get("lease_end_date_max") and
                cleaned_data["lease_end_date_min"] > cleaned_data["lease_end_date_max"]):
            messages.error(self.request, "Min Lease End Date cannot be greater than Max Lease End Date.")
            raise ValidationError("Min Lease End Date cannot be greater than Max Lease End Date.")

        if (cleaned_data.get("move_in_date_min") and cleaned_data.get("move_in_date_max") and
                cleaned_data["move_in_date_min"] > cleaned_data["move_in_date_max"]):
            messages.error(self.request, "Min Move-in Date cannot be greater than Max Move-in Date.")
            raise ValidationError("Min Move-in Date cannot be greater than Max Move-in Date.")

        if (cleaned_data.get("monthly_rent_min") and cleaned_data.get("monthly_rent_max") and
                cleaned_data["monthly_rent_min"] > cleaned_data["monthly_rent_max"]):
            messages.error(self.request, "Min Monthly Rent cannot be greater than Max Monthly Rent.")
            raise ValidationError("Min Monthly Rent cannot be greater than Max Monthly Rent.")

        return cleaned_data
