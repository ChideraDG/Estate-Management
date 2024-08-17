from django.urls import path
from .views import (get_states, view_building_owner_profile,
                    building_owner_dashboard, view_connections)

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('dashboard/<str:pk>/view-bo-profile/', view_building_owner_profile, name='view-building-owner'),
    path('dashboard/bo/<str:pk>/', building_owner_dashboard, name="dashboard-BO"),
    path('dashboard/<str:pk>/view-connections/', view_connections, name="view-connections")
]
