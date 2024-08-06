from django.db import models
from django.core.validators import RegexValidator
from locations.models import Country, State
from django.core.validators import MinValueValidator
from companies.models import Company


class BuildingOwner(models.Model):
    """
    Represents a building owner in the database.

    Attributes:
        building_owner_name (str): The name of the building owner.
        contact_person (str): The name of the contact person for the building owner.
        contact_email (str): The email address of the contact person.
        contact_phone (str): The phone number of the contact person.
        company_id (int): The ID of the company associated with the building owner.
        address (str): The address of the building owner.
        city (str): The city where the building owner is located.
        country (Country): The country where the building owner is located.
        state (State): The state where the building owner is located.
        portfolio_size (int): The size of the building owner's portfolio.
        investment_strategy (str): The investment strategy of the building owner.
        tax_id (str): The tax ID of the building owner.
        notes (str): Any additional notes about the building owner.
        created (datetime): The date and time when the building owner was created.
        updated (datetime): The date and time when the building owner was last updated.

    Examples:
        >>> building_owner = BuildingOwner(
        ...     building_owner_name='John Doe',
        ...     contact_person='Jane Doe',
        ...     contact_email='jane@example.com',
        ...     contact_phone='+1234567890',
        ...     company_id=1,
        ...     address='123 Main St',
        ...     city='Anytown',
        ...     country=Country.objects.get(name='USA'),
        ...     state=State.objects.get(name='California'),
        ...     portfolio_size=10,
        ...     investment_strategy='residential',
        ...     tax_id='1234567890',
        ...     notes='This is a note about the building owner.'
        ... )
        >>> building_owner.save()

    """

    DESIGNATION = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed use'),
    ]

    building_owner_name = models.CharField(max_length=200, blank=False, null=False)
    contact_person = models.CharField(max_length=200, blank=False, null=False)
    contact_email = models.EmailField(unique=True, blank=False, null=False)
    contact_phone = models.CharField(max_length=15, unique=True, blank=False, null=False,
                                     validators=[RegexValidator(
                                         r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                         message="Phone number must be entered in the format: '08012345678' or "
                                                 "'+2348012345678'. Up to 15 digits allowed.")])
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, related_name='building_owner')
    address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='building_owner', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='building_owner', null=True, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    portfolio_size = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1, null=True, blank=True, )
    investment_strategy = models.CharField(max_length=200, choices=DESIGNATION, null=True, blank=True, )
    tax_id = models.CharField(max_length=15, null=True, blank=True, unique=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.building_owner_name

    class Meta:
        ordering = ['updated']
        