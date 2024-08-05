from django.forms import ModelForm
from django import forms
from .models import Company


class CompanyForm(ModelForm):
    """
    A Django form class for creating and editing Company instances.

    The form includes fields for company name, address, phone number, email, website, CAC, logo, and year founded.
    All fields are required except for the website field, which is optional.

    Example usage:

    ```
    # Create a new company form
    form = CompanyForm()

    # Render the form in an HTML template
    return render(request, 'company_form.html', {'form': form})
    ```

    Example usage with initial data:

    ```
    # Get a company instance from the database
    company = Company.objects.get(id=1)

    # Create a company form with initial data
    form = CompanyForm(instance=company)

    # Render the form in an HTML template
    return render(request, 'company_form.html', {'form': form})
    ```
    """

    class Meta:
        """
        Meta class for the CompanyForm.

        Attributes:
            model (Company): The model that this form is based on.
            fields (list): A list of field names that should be included in the form.
            help_texts (dict): A dictionary of help texts for each field.
            widgets (dict): A dictionary of widget classes for each field.
            labels (dict): A dictionary of labels for each field.
        """
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
        