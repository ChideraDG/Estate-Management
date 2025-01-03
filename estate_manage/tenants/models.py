from django.db import models
from users.models import Profile
from locations.models import Country, State
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from apartments.models import Apartment
from houses.models import House
from building_owners.models import BuildingOwner
from estates.models import Estate
from companies.models import Company
    

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

    user = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                related_name='tenant')
    building_owner = models.ForeignKey(BuildingOwner, on_delete=models.CASCADE, blank=True, null=True, 
                                       default=None, related_name='tenants')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, 
                               default=None, related_name='tenants')
    house = models.ForeignKey(House, on_delete=models.SET_NULL, blank=True, null=True, default= None,
                              related_name='tenant_house')
    apartment = models.OneToOneField(Apartment, on_delete=models.SET_NULL, blank=True, null=True, related_name='tenant_apartment') 
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True,
                                     validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                         message="Phone number must be entered in the format: '08012345678' or "
                                                 "'+2348012345678'. Up to 15 digits allowed.")])  
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='tenant', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='tenant', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='tenants-profile-pics/', 
                                        default='person_1.jpg')
    move_in_date = models.DateField(null=True, blank=True)
    lease_start_date = models.DateField(null=True, blank=True)
    lease_end_date = models.DateField(null=True, blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    lease_term = models.CharField(max_length=50, choices=LEASETERM, null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENTSTAT, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    emergency_contact_number = models.CharField(max_length=50, null=True, blank=True, default=None,
                                                validators=[RegexValidator(
                                                    r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                                    message="Phone number must be entered in the format: '08012345678' or "
                                                            "'+2348012345678'. Up to 15 digits allowed.")])  
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENTSTAT, null=True,blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ["-created"]
