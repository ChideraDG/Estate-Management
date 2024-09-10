from django.db import models
from django.core.validators import RegexValidator
from users.models import Profile
from locations.models import Country, State
from django.core.validators import MinValueValidator
from companies.models import Company
from django.core.exceptions import ValidationError


def validate_image_size(value):
    """
    Validates the size of an uploaded image.

    Args:
        value (File): The uploaded image file.

    Raises:
        ValidationError: If the file size exceeds the maximum allowed size (1 MB).

    Example:
        >>> from django.core.files.uploadedfile import UploadedFile
        >>> file = UploadedFile(file='path/to/image.jpg', name='image.jpg', size=1024*1024*2)
        >>> validate_image_size(file)
        ValidationError: Maximum file size allowed is 1.0 MB
    """
    filesize = value.size

    limit = 500 * 1024
    
    if filesize > limit:
        raise ValidationError(f"Maximum file size allowed is {limit / (1024)} KB")


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
        portfolio_size (int): Number of properties owned by the building owner.
        investment_strategy (str): The investment strategy of the building owner.
        tax_id (str): The tax ID of the building owner.
        notes (str): Any additional notes about the building owner.
        unread_messages(int): The amountof unread messages a building owner have.
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

    user = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                related_name='building_owner')
    building_owner_name = models.CharField(max_length=200, blank=False, null=False)
    contact_email = models.EmailField(unique=True, blank=False, null=False)
    contact_phone = models.CharField(max_length=15, unique=True, blank=True, null=True,
                                     validators=[RegexValidator(
                                         r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                         message="Phone number must be entered in the format: '08012345678' or "
                                                 "'+2348012345678'. Up to 15 digits allowed.")])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='building_owners')
    address = models.TextField(blank=True, null=True)
    profile_pics = models.ImageField(blank=True, null=True, upload_to='building-owner-profile-pics/', 
                                    default='building-owner-profile-pics/dp.jpg')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='building_owners', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='building_owners', null=True, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    portfolio_size = models.PositiveIntegerField(default=0, null=True, blank=True)
    investment_strategy = models.CharField(max_length=200, choices=DESIGNATION, null=True, blank=True)
    tax_id = models.CharField(max_length=15, null=True, blank=True, unique=True)
    notes = models.TextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)
    unread_messages = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.building_owner_name

    class Meta:
        ordering = ['updated']
        