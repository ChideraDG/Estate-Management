from django.urls import path
from .views import *

urlpatterns = [
    path("create/", createProfile, name='create-profile'),
    path('home/', home, name='home'),
    path('update/<str:pk>/', updateProfile, name='update-profile'),
    path('delete/<str:pk>/', deleteProfile, name='delete-profile'),
    path('view/<str:pk>/', viewProfile, name='view-profile'),
]
