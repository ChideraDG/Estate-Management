from django.db import models
from django.core.validators import RegexValidator
from users.models import Profile


class Profile(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, default='')
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.TextField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=15, unique=True, blank=True, null=True,
                              validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')])
    email = models.EmailField(unique=True, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    cac = models.CharField(max_length=200, blank=True, null=True)
    logo = models.FileField(blank=True, null=True)
    year_founded = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
