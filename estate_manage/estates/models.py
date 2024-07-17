import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Create your models here.

class Profile(models.Model):
    DESIGNATION = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed use'),
    ]

    AMENITIES = [
        ('parking', 'Parking'),
        ('gym', 'Gym'),
        ('swimming_pool', 'Swimming pool'),
        ('cafeteria', 'Cafeteria'),
        ('spa', 'Spa'),
        ('playground', 'Playground'),
        ('terraces', 'Terraces'),
        ('helipads', 'Helipads'),
        ('package_locker', 'Package locker'),
        ('pet_friendly_amenities', 'Pet-Friendly Amenities'),
        ('laundry_facilities', 'Laundry facilities'),
    ]

    SECURITY = [
        ('perimeter_security', 'Perimeter Security'),
        ('access_control_systems', 'Access Control Systems'),
        ('surveillance_technology', 'Surveillance Technology'),
        ('interior_security_measures', 'Interior Security Measures',),
        ('balancing_visibility_and_discretion', 'Balancing Visibility and Discretion'),
        ('regular_audits_and_assessments', 'Regular Audits and Assessments'),
    ]

    UTILITIES= [
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
        ('sewage', 'Sewage'),
        ('security', 'Security'),
        ('elevator', 'Elevator'),
        ('trash_collection', 'Trash Collection'),
        ('garbage_collection', 'Garbage Collection'),
     ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    estate_name = models.CharField(max_length=100, blank=False, null=False)
    estate_location = models.TextField(null=False, blank=False)
    estate_type = models.CharField(max_length=100, choices=DESIGNATION, blank=False, null=False)
    estate_image = models.ImageField(null=False, blank=False)
    year_built = models.DateField(null=False, blank=False)
    number_of_houses = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    number_of_apartments = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    total_area_covered = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00, validators=[MinValueValidator(0)])
    land_area = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00, validators=[MinValueValidator(0)])
    total_floor_number = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    estate_parking_spaces = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    amenities =MultiSelectField( choices=AMENITIES, null=False, blank=False)
    construction_type = models.CharField(max_length=50,  null=False, blank=False)
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(0)])
    security_features = MultiSelectField(choices=SECURITY, null=False, blank=False)
    utility = MultiSelectField(choices=UTILITIES, null=False, blank=False)
    current_occupancy = models.IntegerField( null=False, blank=False, validators=[MinValueValidator(0)])
    vacancy_rate = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0)])
    estate_description = models.TextField()

    def __str__(self) -> str:
        return self.estate_name
    