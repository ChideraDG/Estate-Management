from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


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
        unread_messages(int): The amountof unread messages a building owner have.
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
    unread_messages = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    

class ActivityLog(models.Model):
    """
    A model to log user activities on the website.

    Attributes
    ----------
    ACTION_CHOICES : list of tuple
        A list of possible actions users can perform.
    ENTITY_CHOICES : list of tuple
        A list of different entities that can be associated with an activity.
    user : ForeignKey
        Reference to the User who performed the activity.
    action_type : CharField
        Type of action performed (e.g., 'LOGIN', 'CREATE').
    entity_type : CharField
        Type of entity involved in the activity (e.g., 'HOUSE', 'FINANCE').
    entity_id : IntegerField
        Optional ID of the specific entity record involved in the activity.
    description : TextField
        Detailed description of the activity.
    timestamp : DateTimeField
        Timestamp when the activity was recorded.

    Methods
    -------
    __str__()
        Returns a string representation of the activity log entry.

    Meta:
        Ordering and verbose name settings for the Django admin.
    """
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
        ('DOWNLOAD', 'Download'),
        ('UPLOAD', 'Upload'),
        ('PAYMENT', 'Payment'),
        ('OTHER', 'Other'),
    ]
    
    ENTITY_CHOICES = [
        ('FINANCE', 'Finance'),
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('MAINTENANCE', 'Maintenance'),
        ('LEASE', 'Lease Agreement'),
        ('DOCUMENT', 'Document'),
        ('GENERAL', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, blank=True, null=True)
    colour = models.CharField(max_length=20, blank=True, null=True)
    entity_type = models.CharField(max_length=20, choices=ENTITY_CHOICES, blank=True, null=True)
    entity_id = models.CharField(max_length=100, null=True, blank=True)  # To associate the activity with a specific entity record
    description = models.TextField()  # Detailed description of the activity
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the activity log entry.

        Returns
        -------
        str
            String representation of the activity log in the format 
            'username action_type entity_type on timestamp'.
        """
        return f'{self.user.username} {self.action_type} {self.entity_type} on {self.timestamp}'

    class Meta:
        """
        Meta options for the ActivityLog model.

        Attributes
        ----------
        ordering : list
            Orders the records by timestamp in descending order.
        verbose_name : str
            Human-readable name for the model in singular form.
        verbose_name_plural : str
            Human-readable name for the model in plural form.
        """
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    @property
    def entity_id_as_list(self):
        # Return the field value as a list, split by commas
        return self.entity_id.split(',')
