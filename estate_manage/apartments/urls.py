from django.urls import path
from .views import house_apartments, view_apartments

urlpatterns = [
    path('<str:type>/<str:pk>/apartment-control/', house_apartments, name='house-apartments'),
    path('<str:type>/<str:pk>/<str:house_id>/apartments/', view_apartments, name='view-apartments'),
]
