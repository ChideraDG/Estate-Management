import uuid
from django.core.validators import MinValueValidator
from django.db import models
from companies.models import Company


class Estate(models.Model):
    DESIGNATION = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed_use', 'Mixed use'),
    ]

    CONSTRUCTION_TYPES = [
        ('fire_resistive', 'Fire Resistive'),
        ('non_combustible', 'Non-Combustible'),
        ('ordinary', 'Ordinary'),
        ('heavy_timber', 'Heavy Timber'),
        ('wood_frame', 'Wood Frame'),
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

    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='estates')
    estate_name = models.CharField(max_length=100, blank=False, null=False)
    estate_location = models.TextField(null=False, blank=False)
    estate_type = models.CharField(max_length=100, choices=DESIGNATION, blank=False, null=False)
    year_built = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1900)])
    number_of_houses = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    number_of_apartments = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    total_area_covered = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00,
                                             validators=[MinValueValidator(0)])
    land_area = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00,
                                    validators=[MinValueValidator(0)])
    total_floor_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    estate_parking_spaces = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    amenities = models.ManyToManyField('Amenity', default='', blank=True)
    construction_type = models.CharField(max_length=50, choices=CONSTRUCTION_TYPES, null=True, blank=True, )
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           validators=[MinValueValidator(0)], default=0.00)
    security_features = models.ManyToManyField('SecurityFeatures', default='', blank=True)
    utilities = models.ManyToManyField('Utility', default='', blank=True)
    current_occupancy = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    vacancy_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00,
                                       validators=[MinValueValidator(0)])
    estate_description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.estate_name


class Amenity(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SecurityFeatures(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Utility(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/estate_photos/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Photo of {self.estate.name}"
