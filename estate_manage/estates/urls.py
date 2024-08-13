from django.urls import path
from .views import *

urlpatterns = [
    path("create/", createEstate, name='create-estate'),
    path('estate-home/', homeEstate, name='home-estate'),
    path('update/<str:pk>/', updateEstate, name='update-estate'),
    path('delete/<str:pk>/', deleteEstate, name='delete-estate'),
    path('view/<str:pk>/', viewEstate, name='view-estate'),
    path('get-states', get_states, name='get-states')
]
