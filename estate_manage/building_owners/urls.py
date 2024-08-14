from django.urls import path
from .views import get_states, update_profile, view_profile, building_owner_dashboard

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('dashboard/<str:pk>/update-bo-profile/', update_profile, name='update-building-owner'),
    path('dashboard/<str:pk>/view-bo-profile/', view_profile, name='view-building-owner'),
    path('dashboard/<str:pk>/', building_owner_dashboard, name="dashboard-BO"),
]
