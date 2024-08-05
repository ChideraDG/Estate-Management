from django.core.validators import MinValueValidator
from django.db import models
from companies.models import Company
from locations.models import Country, State


class Estate(models.Model):
    """
    Represents a real estate property.

    Attributes:
        company (Company): The company that owns the estate.
        estate_name (str): The name of the estate.
        estate_location (str): The location of the estate.
        estate_type (str): The type of the estate (residential, commercial, mixed_use).
        year_built (int): The year the estate was built.
        number_of_houses (int): The number of houses in the estate.
        number_of_apartments (int): The number of apartments in the estate.
        total_area_covered (float): The total area covered by the estate.
        land_area (float): The land area of the estate.
        total_floor_number (int): The total number of floors in the estate.
        estate_parking_spaces (int): The number of parking spaces in the estate.
        amenities (ManyToManyField): The amenities available in the estate.
        construction_type (str): The type of construction used in the estate.
        maintenance_cost (float): The maintenance cost of the estate.
        security_features (ManyToManyField): The security features available in the estate.
        utilities (ManyToManyField): The utilities available in the estate.
        current_occupancy (int): The current occupancy of the estate.
        vacancy_rate (float): The vacancy rate of the estate.
        estate_description (str): A description of the estate.
        country (Country): The country where the estate is located.
        state (State): The state where the estate is located.
        city (str): The city where the estate is located.
        created (datetime): The date and time the estate was created.
        updated (datetime): The date and time the estate was last updated.

    Examples:
        >>> estate = Estate(estate_name='My Estate', estate_location='123 Main St', estate_type='residential', year_built=2000)
        >>> estate.save()
    """
    
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
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='estates', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='estates', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
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
    image = models.ImageField(upload_to='estate_photos/', default='estate_photos/default.jpg')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Photo of {self.estate.name}"
