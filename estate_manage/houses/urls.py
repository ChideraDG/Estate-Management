from django.urls import path
from .views import get_states, houses, house_details, delete_house

urlpatterns = [
    path('get_states/', get_states, name='get-states'),
    path('<str:type>/<str:pk>/houses/', houses, name='houses'),
    path('<str:type>/<str:pk>/houses/<str:house_id>/', house_details, name="house-details"),
    path('delete-house/<str:pk>/', delete_house, name="delete-house"),
]
