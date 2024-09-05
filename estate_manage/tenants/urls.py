from django.urls import path
from .views import (get_states, view_connections, tenantDashboard,
                                tenant_profile, tenants_profiles, tenant_detail,
                                delete_tenant)

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('tenant/<str:pk>/t-profile/', tenant_profile, name='view-tenant'),
    path('tenant/<str:pk>/view-connections/', view_connections, name='t-view-connections'),
    path('tenant/<str:pk>/', tenantDashboard, name='dashboard-T'),
    path('<str:type>/<str:pk>/tenants-profiles/', tenants_profiles, name='tenants-profiles'),
    path('<str:type>/<str:pk>/<str:tenant_id>/details/', tenant_detail, name='tenant-detail'),
    path('delete-tenant/<pk>/', delete_tenant, name="delete-tenant"),
]
