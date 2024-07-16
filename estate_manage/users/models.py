from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?[0-9]{3} ?[0-9-]{8,11}$')],
                                    unique=True, null=True, blank=True)
    designation = models.CharField(max_length=10, null=False, blank=False, default='agent')
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile-pics/',
                                      default='profile-pics/users-default.png')
    state_of_residence = models.CharField(max_length=50, null=True, blank=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    social_github = models.CharField(max_length=500, null=True, blank=True)
    social_twitter = models.CharField(max_length=500, null=True, blank=True)
    social_linkedin = models.CharField(max_length=500, null=True, blank=True)
    social_youtube = models.CharField(max_length=500, null=True, blank=True)
    social_website = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
