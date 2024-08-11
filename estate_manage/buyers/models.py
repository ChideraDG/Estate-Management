from django.db import models
from django.contrib.auth.models import User
from locations.models import Country, State
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
    

class Buyer(models.Model):
    """
    Represents a buyer in the estate management system.

    Attributes:
        user (User): The user associated with the buyer profile.
        full_name (str): The full name of the buyer.
        email (str): The email address of the buyer.
        phone_number (str): The contact number of the buyer.
        address (str): The current residential address of the buyer.
        country (Country): The country of residence of the buyer.
        state (State): The state of residence of the buyer.
        city (str): The city of residence of the buyer.
        budget (float): The budget range the buyer is willing to spend on a property.
        preferred_property_type (str): The type of property the buyer is interested in (e.g., residential, commercial).
        preferred_location (str): The location or area where the buyer is interested in buying property.
        notes (str): Additional notes or preferences specified by the buyer.
        created (datetime): The date and time the buyer profile was created.
        updated (datetime): The date and time the buyer profile was last updated.

    Examples:
        >>> buyer = Buyer(full_name="John Doe", email="john@example.com", phone_number="1234567890")
        >>> buyer.save()
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='buyers/', null=True, blank=True, validators=[validate_image_size])
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    preferred_property_type = models.CharField(max_length=100, choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed Use')
    ])
    preferred_location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the buyer.

        Returns:
            str: The full name of the buyer.
        """
        return self.full_name
