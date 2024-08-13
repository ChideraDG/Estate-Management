from django.urls import path
from .views import *

urlpatterns = [
    path('building-owner-home/', buildingOwnersHome, name='building-owner-home'),
    path('get_states/', get_states, name='get-states'),
    path('create/', createProfile, name='create-building-owner'),
    path('update/<str:pk>/', updateProfile, name='update-building-owner'),
    path('view/<str:pk>/', viewProfile, name='view-building-owner'),
    path('delete/<str:pk>/', deleteProfile, name='delete-building-owner'),
    path('<str:pk>/', buildingOwnerDashboard, name="dashboard-BO"),
]
