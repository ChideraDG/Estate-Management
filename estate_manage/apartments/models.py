from django.db import models
from locations.models import Country, State
from django.core.validators import MinValueValidator
from houses.models import House



class Apartment(models.Model):
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

    PET = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, null=True, related_name='apartment')
    apartment_number = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)], default=0)
    floor_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name='apartment', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, related_name='apartment', null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    apartment_size =  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00,
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
        return str(self.apartment_number)
    

class Photo(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='apartment_photos/', default='apartment_photos/default.jpg')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
        Returns a string representation of the photo.

        Returns:
            str: "Photo of <Apartment number>".
        """
        return f"Photo of {self.apartment.apartment_number}"
    