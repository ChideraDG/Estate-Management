from django.db import models
from django.core.validators import RegexValidator

# Create your models here
class Company(models.Model):
    com_name= models.CharField(max_length = 100, blank= False, null= False)
    com_address = models.TextField(max_length=200, blank=False, null=False)
    com_number = models.CharField(max_length =15, unique=True, 
                                  validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')])
    com_mail = models.EmailField(unique=True, blank= False, null=False)
    com_web = models.CharField(max_length=200, blank=True, null=False)
    com_cac = models.CharField(max_length=200, blank= False, null=False)
    com_logo = models.FileField(blank= False, null=False)
    com_year_founded= models.CharField(max_length= 50, blank=False, null= False)
    
    def __str__(self):
        return self.com_name