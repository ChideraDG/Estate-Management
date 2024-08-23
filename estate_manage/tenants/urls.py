from django.urls import path
from .views import (get_states, view_connections, tenantDashboard,
                                tenant_profile)

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('tenant/<str:pk>/t-profile/', tenant_profile, name='view-tenant'),
    path('tenant/<str:pk>/view-connections/', view_connections, name='t-view-connections'),
    path('tenant/<str:pk>/', tenantDashboard, name='dashboard-T'),
]
