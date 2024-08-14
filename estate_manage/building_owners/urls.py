from django.urls import path
from .views import *

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('update/<str:pk>/', updateProfile, name='update-building-owner'),
    path('dashboard/<str:pk>/view-bo-profile/', viewProfile, name='view-building-owner'),
    path('<str:pk>/', buildingOwnerDashboard, name="dashboard-BO"),
]
