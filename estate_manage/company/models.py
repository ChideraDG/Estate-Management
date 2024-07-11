from django.db import models

# Create your models here
class Company(models.Model):
    com_name= models.CharField(max_length = 100, blank= False, null= False)
    com_address = models.TextField(max_length= 200, blank = False, null= False)
    com_number = models.CharField(max_length = 100, blank = False, null = False )
    com_mail = models.CharField(max_length = 100, blank= False, null= False)
    com_web = models.CharField(max_length = 200, blank = True, null = False)
    com_cac = models.CharField(max_length = 200, blank = False, null  = False)
    com_logo = models.FileField(blank= False, null= False)
    com_year_founded= models.CharField(max_length= 50, blank = False, null= False)
    
    def __str__(self) -> str:
        return self.com_name