from django.db import models
from django.core.validators import RegexValidator
from users.models import Profile


class Company(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, default='')
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.TextField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=15, unique=True, blank=True, null=True,
                              validators=[RegexValidator(
                                  r'^\+?[0-9]{3} ?[0-9-]{8,11}$',
                                  message="Phone number must be entered in the format: '08012345678' or "
                                          "'+2348012345678'. Up to 15 digits allowed.")])
    email = models.EmailField(unique=True, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    cac = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True, upload_to='company-logo/', default="company-logo/default.svg")
    year_founded = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
