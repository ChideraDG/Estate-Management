from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from apartments.models import Apartment
from users.models import Profile


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
    
    
class Agent(models.Model):
    """
    A model representing an agent who manages apartments within the estate management system.

    Attributes
    ----------
    EMPLOYMENT_STATUS_CHOICES : list of tuple
        A list of tuples representing the employment status options.
    name : str
        The full name of the agent.
    email : str
        The unique email address of the agent.
    phone_number : str, optional
        The primary phone number of the agent with validation.
    profile_picture : ImageField, optional
        The profile picture of the agent.
    bio : str, optional
        A short biography or description of the agent.
    alternate_phone_number : str, optional
        An additional contact number for the agent.
    address : str, optional
        The residential address of the agent.
    date_of_hire : date, optional
        The date when the agent was hired.
    employment_status : str
        The current employment status of the agent, defaults to 'active'.
    number_of_apartments_managed : int, optional
        The number of apartments currently managed by the agent, defaults to 0.
    rating : float, optional
        The rating of the agent, ranging from 0.0 to 5.0.
    linkedin_url : str, optional
        The URL to the agent's LinkedIn profile.
    twitter_url : str, optional
        The URL to the agent's Twitter profile.
    apartments : ManyToManyField
        The many-to-many relationship with the `Apartment` model.
    created : datetime
        The date and time when the agent record was created.
    updated : datetime
        The date and time when the agent record was last updated.

    Methods
    -------
    __str__() -> str
        Returns the name of the agent.
    """

    EMPLOYMENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True, default='',
                                related_name='agents')
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True,
                                    validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                        message="Phone number must be entered in the format: '08012345678' or "
                                                "'+2348012345678'. Up to 15 digits allowed.")])
    profile_picture = models.ImageField(upload_to='agents/', null=True, blank=True, 
                                        validators=[validate_image_size], default='agents/dp.jpg')
    bio = models.TextField(null=True, blank=True)
    alternate_phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_hire = models.DateField(null=True, blank=True)
    employment_status = models.CharField(max_length=10, choices=EMPLOYMENT_STATUS_CHOICES, default='active')
    number_of_apartments_managed = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, 
                                 validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    apartments = models.ManyToManyField(Apartment, related_name='agents')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the Agent instance.

        Returns
        -------
        str
            The name of the agent.
        """
        return self.name
