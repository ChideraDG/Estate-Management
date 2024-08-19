from django.urls import path
from .views import *

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('bo/<str:pk>/houses/', building_owner_houses, name='bo-houses'),
]
