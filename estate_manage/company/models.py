from django.db import models
from django.core.validators import RegexValidator


class Profile(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.TextField(max_length=200, blank=False, null=False)
    number = models.CharField(max_length=15, unique=True,
                              validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')])
    email = models.EmailField(unique=True, blank=False, null=False)
    website = models.CharField(max_length=200, blank=True, null=False)
    cac = models.CharField(max_length=200, blank=False, null=False)
    logo = models.FileField(blank=False, null=False)
    year_founded = models.CharField(max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
