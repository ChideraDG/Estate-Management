from django.urls import path
from .views import  view_connections, buyerDashboard, buyerProfile

urlpatterns = [
    path('company/<str:pk>/view-connections/', view_connections, name='b-view-connections'),
    path('company/<str:pk>/b-profile/', buyerProfile, name='view-buyer'),
    path('buyer/<str:pk>/', buyerDashboard, name='dashboard-B'),
]
