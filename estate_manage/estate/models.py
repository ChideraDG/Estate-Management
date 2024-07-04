from django.core.validators import RegexValidator
from django.db import models


class Registration(models.Model):
    GENDER = [
        ('m', 'Male'),
        ('f', 'Female'),
    ]

    full_name = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=50, choices=GENDER, null=False, blank=False)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=False, null=False)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')])
    state_of_origin = models.CharField(max_length=50, blank=False, null=False)
    state_of_residence = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    address_1 = models.CharField(max_length=200, blank=False, null=False)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)

