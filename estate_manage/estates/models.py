import uuid
from django.core.validators import MinValueValidator
from django.db import models
from company.models import Profile


class Profile(models.Model):
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

    company = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    estate_name = models.CharField(max_length=100, blank=False, null=False)
    estate_location = models.TextField(null=False, blank=False)
    estate_type = models.CharField(max_length=100, choices=DESIGNATION, blank=False, null=False)
    estate_image = models.JSONField(default=list)
    year_built = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1900)])
    number_of_houses = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    number_of_apartments = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    total_area_covered = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00,
                                             validators=[MinValueValidator(0)])
    land_area = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00,
                                    validators=[MinValueValidator(0)])
    total_floor_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    estate_parking_spaces = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    amenities = models.TextField(null=True, blank=True, default='')
    construction_type = models.CharField(max_length=50, choices=CONSTRUCTION_TYPES, null=True, blank=True, )
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           validators=[MinValueValidator(0)], default=0.00)
    security_features = models.TextField(null=True, blank=True, default='')
    utility = models.TextField(null=True, blank=True, default='')
    current_occupancy = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    vacancy_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0.00,
                                       validators=[MinValueValidator(0)])
    estate_description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.estate_name

    def get_amenities_list(self):
        if self.amenities:
            return self.amenities.split(',')
        return []

    def set_amenities_list(self, choices):
        self.amenities = ','.join(choices)

    def get_security_features_list(self):
        if self.security_features:
            return self.security_features.split(',')
        return []

    def set_security_features_list(self, choices):
        self.security_features = ','.join(choices)

    def get_utility_list(self):
        if self.utility:
            return self.utility.split(',')
        return []

    def set_utility_list(self, choices):
        self.utility = ','.join(choices)

    def add_estate_image(self, path):
        self.estate_image.append(path)
        self.save()
