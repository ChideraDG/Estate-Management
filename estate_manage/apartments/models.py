from django.db import models
from locations.models import Country, State
from django.core.validators import MinValueValidator
from houses.models import House


class Apartment(models.Model):
    """
    Represents an apartment within a house in the estate management system.

    Attributes:
        CONDITION (list of tuple): Choices for the condition of the apartment.
        OCCUPANCY (list of tuple): Choices for the occupancy status of the apartment.
        PET (list of tuple): Choices indicating whether pets are allowed in the apartment.

        house (House): The house to which the apartment belongs.
        apartment_number (int): The number of the apartment.
        floor_number (int): The floor on which the apartment is located.
        country (Country): The country where the apartment is located.
        state (State): The state where the apartment is located.
        city (str): The city where the apartment is located.
        apartment_size (Decimal): The size of the apartment in square meters.
        number_of_rooms (int): The number of rooms in the apartment.
        rent_amount (Decimal): The rent amount for the apartment.
        deposit_amount (Decimal): The deposit amount required for the apartment.
        lease_start_date (DateField): The start date of the lease.
        lease_end_date (DateField): The end date of the lease.
        occupancy_status (str): The current occupancy status of the apartment.
        condition (str): The current condition of the apartment.
        pet_allowed (str): Indicates whether pets are allowed in the apartment.
        notes (str): Additional notes or comments about the apartment.
        created (datetime): The date and time when the apartment record was created.
        updated (datetime): The date and time when the apartment record was last updated.

    Examples:
        >>> apartment = Apartment(apartment_number=101, floor_number=1, rent_amount=1000.00)
        >>> apartment.save()
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

    PET = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, null=True, related_name='apartments')
    apartment_number = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)], default=0)
    floor_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='apartments', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='apartments', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    apartment_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                         validators=[MinValueValidator(0)])
    number_of_rooms = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=1)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                      validators=[MinValueValidator(0)])
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
                                         validators=[MinValueValidator(0)])
    lease_start_date = models.DateField(null=True, blank=True)
    lease_end_date = models.DateField(null=True, blank=True)
    occupancy_status = models.CharField(max_length=50, choices=OCCUPANCY, null=True, blank=True)
    condition = models.CharField(max_length=50, choices=CONDITION, null=True, blank=True)
    pet_allowed = models.CharField(max_length=50, choices=PET, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the apartment.

        Returns:
            str: The apartment number.
        """
        return str(self.apartment_number)
 

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
    