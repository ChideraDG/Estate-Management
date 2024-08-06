from django.db import models
from django.core.validators import RegexValidator
from locations.models import Country, State
from django.core.validators import MinValueValidator
from companies.models import Company

# Create your models here.
class BuildingOwner(models.Model):
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
        city = models.CharField(max_length=200, blank=True, null=True)
        country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='building_owner', null=True, blank=True)
        state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='building_owner', null=True, blank=True)
        portfolio_size = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1, null=True, blank=True,)
        investment_strategy = models.CharField(max_length=200, choices=DESIGNATION, null=True, blank=True,)
        tax_id = models.CharField(max_length=15, null=True, blank=True, unique=True)
        notes = models.TextField(blank=True, null=True)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)

        def __str__(self) -> str:
                return self.building_owner_name