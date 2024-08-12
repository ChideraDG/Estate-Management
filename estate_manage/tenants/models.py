from django.db import models
from locations.models import Country, State
from django.core.validators import MinValueValidator
from apartments.models import Apartment
from django.core.validators import RegexValidator
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
    

class Tenant(models.Model):
    LEASETERM = [
        ('yearly', 'Yearly'),
        ('six_monthly', 'Six Monthly'),
        ('month_to_month', 'Month to Month'),
    ]

    PAYMENTSTAT = [
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    EMPLOYMENTSTAT = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('self_employed', 'Self Employed'),
        ('student', 'Student'),
    ]

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False, unique=True,
                                     validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                         message="Phone number must be entered in the format: '08012345678' or "
                                                 "'+2348012345678'. Up to 15 digits allowed.")])  
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='tenant', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='tenant', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='tenants-profile-pics/', 
                             validators=[validate_image_size])
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, null=True, related_name='tenants') 
    move_in_date = models.DateField(null=True, blank=True)
    lease_start_date = models.DateField(null=True, blank=True)
    lease_end_date = models.DateField(null=True, blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    lease_term = models.CharField(max_length=50, choices=LEASETERM, null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENTSTAT, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=50, null=True, blank=True, unique=True,
                                                validators=[RegexValidator(
                                                    r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                                    message="Phone number must be entered in the format: '08012345678' or "
                                                            "'+2348012345678'. Up to 15 digits allowed.")])  
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENTSTAT, null=True,blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
