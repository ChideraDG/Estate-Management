from django.urls import path
from .views import *

urlpatterns = [
    path('house-home/', houseHome, name='house-home'),
    path('get_states/', get_states, name='get-states'),
    path('create/', createHouse, name='create-house'),
    path('update/<str:pk>/', updateHouse, name='update-house'),
    path('view/<str:pk>/', viewHouse, name='view-house'),
    path('delete/<str:pk>/', deleteHouse, name='delete-house'),
]
