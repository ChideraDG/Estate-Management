from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
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

    limit = 1 * 1024 * 1024
    
    if filesize > limit:
        raise ValidationError(f"Maximum file size allowed is {limit / (1024 * 1024)} MB")


class Profile(models.Model):
    """
    Represents a user's profile.

    Attributes:
        user (User): The associated Django User instance.
        name (str): The user's full name.
        username (str): The user's username.
        gender (str): The user's gender (male/female).
        date_of_birth (date): The user's date of birth.
        email (str): The user's email address.
        phone_number (str): The user's phone number.
        designation (str): The user's designation (default: agent).
        bio (str): The user's bio.
        profile_image (File): The user's profile image.
        state_of_residence (str): The user's state of residence.
        address_1 (str): The user's primary address.
        address_2 (str): The user's secondary address.
        social_github (str): The user's GitHub profile URL.
        social_twitter (str): The user's Twitter profile URL.
        social_linkedin (str): The user's LinkedIn profile URL.
        social_youtube (str): The user's YouTube channel URL.
        social_website (str): The user's personal website URL.
        created (datetime): The timestamp when the profile was created.
        updated (datetime): The timestamp when the profile was last updated.

    Example:
        >>> from django.contrib.auth.models import User
        >>> user = User.objects.create_user('john', 'john@example.com', 'password')
        >>> profile = Profile.objects.create(user=user, name='John Doe', username='john')
        >>> profile.email
        'john@example.com'
    """

    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    DESIGNATION = [
        ('', 'Select a Designation'),
        ('buyer', 'Buyer'),
        ('company', 'Company'),
        ('tenant', 'Tenant'),
        ('building_owner', 'Building Owner'),
        ('agent', 'Agent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')],
                                    unique=True, null=True, blank=True)
    designation = models.CharField(max_length=25, null=False, blank=False, default='buyer', choices=DESIGNATION)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile-pics/',
                                      default='profile-pics/dp.jpg',)
    state_of_residence = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    social_github = models.URLField(max_length=500, null=True, blank=True)
    social_twitter = models.URLField(max_length=500, null=True, blank=True)
    social_linkedin = models.URLField(max_length=500, null=True, blank=True)
    social_youtube = models.URLField(max_length=500, null=True, blank=True)
    social_website = models.URLField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    