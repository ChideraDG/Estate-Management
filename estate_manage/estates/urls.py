from django.urls import path
from .views import (get_states, estates, deleteEstate, estate_details, view_estate_houses, estate_houses)

urlpatterns = [
    path('get-states', get_states, name='get-states'),
    path('<str:type>/<str:pk>/estates/', estates, name='estates'),
    path('<str:type>/<str:pk>/estates/<str:estate_id>/', estate_details, name="estate-details"),
    path('delete-estate/<str:pk>/', deleteEstate, name="delete-estate"),
    path('<str:type>/<str:pk>/<str:estate_id>/houses/', view_estate_houses, name='view-houses'),
    path('<str:type>/<str:pk>/house-management/', estate_houses, name='estate-houses'),
]
