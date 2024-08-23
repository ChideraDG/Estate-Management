from django.urls import path
from .views import house_apartments, view_apartments, apartment_details, delete_apartment

urlpatterns = [
    path('<str:type>/<str:pk>/apartment-control/', house_apartments, name='house-apartments'),
    path('<str:type>/<str:pk>/<str:house_id>/apartments/', view_apartments, name='view-apartments'),
    path('<str:type>/<str:pk>/apartments/<str:house_id>/<str:apartment_number>/', apartment_details, name="apartment-details"),
    path('delete/<str:pk>/', delete_apartment, name="delete-apartment")
]
