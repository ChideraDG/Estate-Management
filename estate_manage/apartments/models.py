from django.db import models
from houses.models import House


class Apartment(models.Model):
    """
    Represents an apartment within a house in the estate management system.

    Attributes:
        apartment_number (str): The unique number of the apartment.
        house (House): The house to which the apartment belongs.
        floor_number (int): The floor on which the apartment is located.
        number_of_rooms (int): The number of rooms in the apartment.
        size_in_sqft (Decimal): The size of the apartment in square feet.
        balcony (bool): Indicates if the apartment has a balcony.
        parking_space (bool): Indicates if the apartment has a parking space.
        is_furnished (bool): Indicates if the apartment is furnished.
        number_of_bathrooms (int): The number of bathrooms in the apartment.
        number_of_bedrooms (int): The number of bedrooms in the apartment.
        kitchen_type (str): The type of kitchen in the apartment (Open or Closed).
        flooring_type (str): The type of flooring in the apartment (Tile, Wood, Carpet).
        heating_system (str): The type of heating system (Central, Electric, Gas).
        air_conditioning (bool): Indicates if the apartment has air conditioning.
        water_supply (str): The source of water supply (Public, Well, Borehole).
        electricity_supply (str): The source of electricity supply (Grid, Solar, Generator).
        internet_ready (bool): Indicates if the apartment is internet ready.
        cable_tv_ready (bool): Indicates if the apartment is cable TV ready.
        rent_price (Decimal): The rent price of the apartment.
        sale_price (Decimal): The sale price of the apartment.
        security_deposit (Decimal): The security deposit for the apartment.
        maintenance_fee (Decimal): The maintenance fee for the apartment.
        is_occupied (bool): Indicates if the apartment is occupied.
        tenant (Tenant): The tenant occupying the apartment.
        last_renovation_year (int): The year when the apartment was last renovated.
        condition (str): The current condition of the apartment (New, Good, Needs Renovation).
        maintenance_requests (ManyToMany): Maintenance requests related to the apartment.
        notes (str): Additional notes or comments about the apartment.
        created (datetime): The date and time when the apartment record was created.
        updated (datetime): The date and time when the apartment record was last updated.
    """
    
    # Basic Information
    apartment_number = models.IntegerField(unique=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='apartments', null=True, blank=True)
    floor_number = models.IntegerField(default=1)
    number_of_rooms = models.IntegerField(default=1)
    size_in_sqft = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    balcony = models.BooleanField(default=False)
    parking_space = models.BooleanField(default=False)

    # Apartment Features
    is_furnished = models.BooleanField(default=False)
    number_of_bathrooms = models.IntegerField(null=True, blank=True)
    number_of_bedrooms = models.IntegerField(null=True, blank=True)
    kitchen_type = models.CharField(max_length=50, choices=[('Open', 'Open'), ('Closed', 'Closed')], null=True, blank=True)
    flooring_type = models.CharField(max_length=50, choices=[('Tile', 'Tile'), ('Wood', 'Wood'), ('Carpet', 'Carpet')], null=True, blank=True)
    heating_system = models.CharField(max_length=50, choices=[('Central', 'Central'), ('Electric', 'Electric'), ('Gas', 'Gas')], null=True, blank=True)
    air_conditioning = models.BooleanField(default=False)

    # Utilities
    water_supply = models.CharField(max_length=50, choices=[('Public', 'Public'), ('Well', 'Well'), ('Borehole', 'Borehole')], null=True, blank=True)
    electricity_supply = models.CharField(max_length=50, choices=[('Grid', 'Grid'), ('Solar', 'Solar'), ('Generator', 'Generator')], null=True, blank=True)
    internet_ready = models.BooleanField(default=False)
    cable_tv_ready = models.BooleanField(default=False)

    # Financial Information
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,  default=0.00)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Occupancy Details
    is_occupied = models.BooleanField(default=False)

    # Maintenance & Condition
    last_renovation_year = models.IntegerField(null=True, blank=True)
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Good', 'Good'), ('Needs Renovation', 'Needs Renovation')], null=True, blank=True, default='New')

    # Additional Information
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the apartment.
        
        Returns:
            str: The apartment number and floor number.
        """
        return f"Apartment {self.apartment_number} - Floor {self.floor_number}"

    class Meta:
        ordering = ['apartment_number', 'floor_number']
        unique_together = ('house', 'apartment_number')


class Photo(models.Model):
    """
    Represents a photo associated with an apartment.

    Attributes:
        apartment (Apartment): The apartment to which the photo belongs.
        image (ImageField): The image file of the photo.
        description (str): A brief description of the photo.

    Examples:
        >>> photo = Photo(apartment=some_apartment_instance, image='path/to/image.jpg', description='Living room view')
        >>> photo.save()
    """

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='apartment_photos/', default='apartment_photos/default.jpg')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
        Returns a string representation of the photo.

        Returns:
            str: A description of the photo, including the apartment number.
        """
        return f"Photo of {self.apartment.apartment_number}"
    