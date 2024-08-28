from django.urls import path
from .views import (get_states, building_owner_profile, get_apartments,
                    building_owner_dashboard, view_connections, tenant_profiles)

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('get_apartments/', get_apartments, name='get-apartments'),
    path('bo/<str:pk>/bo-profile/', building_owner_profile, name='view-building-owner'),
    path('bo/<str:pk>/', building_owner_dashboard, name="dashboard-BO"),
    path('bo/<str:pk>/view-connections/', view_connections, name="bo-view-connections"),
    path('bo/<str:pk>/tenant-profiles/', tenant_profiles, name='bo-tenant-profiles')
]
