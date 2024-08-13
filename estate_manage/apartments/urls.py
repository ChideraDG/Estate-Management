from django.urls import path
from .views import *

urlpatterns = [
    path('apartment-home/', apartmentHome, name='apartment-home'),
    path('get_states/', get_states, name='get-states'),
    path('create/', createApartment, name='create-apartment'),
    path('update/<str:pk>/', updateApartment, name='update-apartment'),
    path('view/<str:pk>/', viewApartment, name='view-apartment'),
    path('delete/<str:pk>/', deleteApartment, name='delete-apartment'),
]
