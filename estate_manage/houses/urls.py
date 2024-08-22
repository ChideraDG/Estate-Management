from django.urls import path
from .views import get_states, building_owner_houses, house_details, delete_house

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('bo/<str:pk>/houses/', building_owner_houses, name='bo-houses'),
    path('bo/<str:pk>/houses/<str:house_id>/', house_details, name="house-details"),
    path('delete-house/<str:pk>/', delete_house, name="delete-house"),
]
