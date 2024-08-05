from django.db import models
from django.core.validators import RegexValidator
from users.models import Profile


class Company(models.Model):
    """
    Represents a company in the database.

    Attributes:
        owner (Profile): The owner of the company. Can be blank or null.
        name (str): The name of the company. Cannot be blank or null.
        address (str): The address of the company. Can be blank or null.
        number (str): The phone number of the company. Can be blank or null. Must be in the format '08012345678' or '+2348012345678'.
        email (str): The email address of the company. Can be blank or null. Must be unique.
        website (str): The website of the company. Can be blank or null.
        cac (str): The CAC number of the company. Can be blank or null.
        logo (ImageField): The logo of the company. Can be blank or null. Defaults to 'company-logo/default.svg'.
        year_founded (str): The year the company was founded. Can be blank or null.
        created (datetime): The date and time the company was created. Automatically set when the company is created.
        updated (datetime): The date and time the company was last updated. Automatically set when the company is updated.

    Examples:
        >>> company = Company(name='Example Company', address='123 Main St', number='08012345678', email='example@example.com')
        >>> company.save()
        >>> company.owner
        None
        >>> company.name
        'Example Company'
        >>> company.address
        '123 Main St'
        >>> company.number
        '08012345678'
        >>> company.email
        'example@example.com'
    """

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, default='',
                              related_name='companies')
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.TextField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=15, unique=True, blank=True, null=True,
                              validators=[RegexValidator(
                                  r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                  message="Phone number must be entered in the format: '08012345678' or "
                                          "'+2348012345678'. Up to 15 digits allowed.")])
    email = models.EmailField(unique=True, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    cac = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True, upload_to='company-logo/', default="company-logo/default.svg")
    year_founded = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    