from django.urls import path
from .views import (get_states, building_owner_profile,
                    building_owner_dashboard, view_connections,
                    building_owner_houses)

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('bo/<str:pk>/bo-profile/', building_owner_profile, name='view-building-owner'),
    path('bo/<str:pk>/', building_owner_dashboard, name="dashboard-BO"),
    path('bo/<str:pk>/view-connections/', view_connections, name="view-connections"),
    path('bo/<str:pk>/houses/', building_owner_houses, name='bo-houses'),
]
