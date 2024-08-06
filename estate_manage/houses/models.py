from django.db import models
from django.core.validators import RegexValidator
from locations.models import Country, State
from django.core.validators import MinValueValidator
from estates.models import Estate
from building_owners.models import BuildingOwner
from estates.models import Utility

# Create your models here.

# class House(models.Model):
#     estate = models.ForeignKey(Estate, on_delete=models.CASCADE, blank=True, null=True, related_name='house')