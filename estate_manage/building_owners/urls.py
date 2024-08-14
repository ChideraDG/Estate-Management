from django.urls import path
from .views import *

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('dashboard/<str:pk>/update-bo-profile/', updateProfile, name='update-building-owner'),
    path('dashboard/<str:pk>/view-bo-profile/', viewProfile, name='view-building-owner'),
    path('dashboard/<str:pk>/', buildingOwnerDashboard, name="dashboard-BO"),
]
