from django.db import models
from locations.models import Country, State
from django.core.validators import MinValueValidator
from estates.models import Estate
from building_owners.models import BuildingOwner
from agents.models import Agent


class House(models.Model):
    """
    Represents a house in the estate management system.

    Attributes:
        estate (Estate): The estate to which the house belongs.
        building_owner (BuildingOwner): The owner of the building.
        house_number (int): The unique number assigned to the house.
        address (str): The full address of the house.
        country (Country): The country where the house is located.
        state (State): The state where the house is located.
        city (str): The city where the house is located.
        house_size (float): The size of the house in square meters or other relevant units.
        number_of_apartments (int): The number of separate apartments within the house.
        total_floor_number (int): The total number of floors in the house.
        house_garage_space (int): The number of garage spaces available in the house.
        yard_size (float): The size of the yard associated with the house.
        renovation_year (str): The year the house was last renovated.
        condition (str): The current condition of the house (e.g., new, renovated, requires maintenance).
        features (ManyToManyField): A list of features available in the house (e.g., pool, fireplace).
        utilities (ManyToManyField): A list of utilities available in the house (e.g., electricity, water).
        sale_price (float): The sale price of the house.
        rent_price (float): The rental price of the house.
        occupancy_status (str): The current occupancy status of the house (e.g., occupied, vacant).
        notes (str): Additional notes about the house.
        created (datetime): The date and time when the house record was created.
        updated (datetime): The date and time when the house record was last updated.

    Examples:
        >>> house = House(house_number=123, address='456 Elm St', city='Springfield', sale_price=250000)
        >>> house.save()
    """
    
    CONDITION = [ 
        ('new', 'New'),
        ('renovated', 'Renovated'),
        ('requires_maintenance', 'Requires Maintenance'),
    ]

    OCCUPANCY = [
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
        ('under_renovation', 'Under Renovation'),
    ]

    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, blank=True, null=True, related_name='houses')
    building_owner = models.ForeignKey(BuildingOwner, on_delete=models.CASCADE, blank=True, null=True, related_name='houses')
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='houses', blank=True, null=True)
    house_number = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    address = models.TextField(blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='houses', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='houses', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    house_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00, validators=[MinValueValidator(0)])
    number_of_apartments = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    number_of_floors = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    garage_space = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    yard_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00, validators=[MinValueValidator(0)])
    renovation_year = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION, null=False, blank=False, default='new')
    features = models.ManyToManyField('Feature', default='', blank=True)
    utilities = models.ManyToManyField('Utility', default='', blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00, validators=[MinValueValidator(0)])
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00, validators=[MinValueValidator(0)])
    occupancy_status = models.CharField(max_length=50, choices=OCCUPANCY, null=False, blank=False, default="vacant")
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.house_number}, {self.address}'
    
    class Meta:
        ordering = ['-created']  # to order the houses from latest to oldest.
        unique_together = ('house_number', 'address')


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
    """
    Represents a feature available in a house.

    Attributes:
        code (str): A unique code for the feature.
        name (str): The name of the feature.

    Examples:
        >>> feature = Feature(code='FP', name='Fireplace')
        >>> feature.save()
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        Returns the name of the feature.

        Returns:
            str: The name of the feature.
        """
        return self.name


class Photo(models.Model):
    """
    Represents a photo associated with a house.

    Attributes:
        house (House): The house that the photo is associated with.
        image (ImageField): The image file of the photo.
        description (str): A description of the photo.

    Examples:
        >>> house = House.objects.get(id=1)
        >>> photo = Photo(house=house, image='house_photos/house1.jpg', description='Front view')
        >>> photo.save()
    """
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='house_photos/', default='house_photos/default.jpg')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
        Returns a string representation of the photo.

        Returns:
            str: "Photo of <House number>".
        """
        return f"Photo of {self.house.house_number}"
