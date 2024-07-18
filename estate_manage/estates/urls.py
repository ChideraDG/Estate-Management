from django.urls import path
from .views import *

urlpatterns = [
    path("", createProfile, name='create-profile'),
]
