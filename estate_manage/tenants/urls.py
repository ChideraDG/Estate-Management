from django.urls import path
from .views import *

urlpatterns = [
    path('tenant-home/', tenantHome, name='tenant-home'),
    path('get_states/', get_states, name='get-states'),
    path('create/', createTenant, name='create-tenant'),
    path('update/<str:pk>/', updateTenant, name='update-tenant'),
    path('view/<str:pk>/', viewTenant, name='view-tenant'),
    path('delete/<str:pk>/', deleteTenant, name='delete-tenant'),
    path('<str:pk>/', tenantDashboard, name='T_dashboard'),
]
