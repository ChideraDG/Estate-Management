from django.db import models
from locations.models import Country, State
from django.core.validators import MinValueValidator
from estates.models import Estate
from building_owners.models import BuildingOwner

# Create your models here.

class House(models.Model):
    CONDITION = [ 
        ('new', 'New'),
        ('renovated', 'Renovated'),
        ('requires_maintenance', 'Requires Maintenance'),
    ]

    OCCUPANCY = [
        ('occupied', 'Ocuupied'),
        ('vacant', 'Vacant'),
        ('under_renovation', 'Under Renovation'),
    ]

    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, blank=True, null=True, related_name='house')
    building_owner = models.ForeignKey(BuildingOwner, on_delete=models.CASCADE, blank=True, null=True, related_name='house')
    house_number = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    address = models.TextField(blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='house', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='house', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    house_size =  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    number_of_apartments = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    total_floor_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    house_garage_space = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    yard_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    renovation_year = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION, null=True, blank=True)
    features = models.ManyToManyField('Feature', default='', blank=True)
    utilities = models.ManyToManyField('Utility', default='', blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                             validators=[MinValueValidator(0)])
    occupancy_status = models.CharField(max_length=50, choices=OCCUPANCY, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.house_number)



class Utility(models.Model):
    """
    Represents a utility that an estate can have.

    Attributes:
        code (str): Unique code for the utility (max length 50).
        name (str): Name of the utility (max length 100).

    Example:
        >>> utility = Utility(code="ELEC", name="Electricity")
        >>> print(utility)
        Electricity
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the utility.

        Returns:
            str: Name of the utility.
        """
        return self.name
    
class Feature(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Photo(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='house_photos/', default='house_photos/default.jpg')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
        Returns a string representation of the photo.

        Returns:
            str: "Photo of <House number>".
        """
        return f"Photo of {self.house.house_number}"
    
