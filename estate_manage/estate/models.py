from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Registration(models.Model):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    DESIGNATION = [
        ('company', 'Company'),
        ('tenant', 'Tenant')
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')],
                                    unique=True, null=True, blank=True)
    designation = models.CharField(max_length=10, choices=DESIGNATION, null=False, blank=False, default='tenant')
    state_of_origin = models.CharField(max_length=50, null=True, blank=True)
    state_of_residence = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
