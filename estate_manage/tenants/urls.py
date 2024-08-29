from django.urls import path
from .views import (get_states, view_connections, tenantDashboard,
                                tenant_profile, tenants_profiles)

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('tenant/<str:pk>/t-profile/', tenant_profile, name='view-tenant'),
    path('tenant/<str:pk>/view-connections/', view_connections, name='t-view-connections'),
    path('tenant/<str:pk>/', tenantDashboard, name='dashboard-T'),
    path('<str:type>/<str:pk>/tenant-profiles/', tenants_profiles, name='tenants-profiles')
]
