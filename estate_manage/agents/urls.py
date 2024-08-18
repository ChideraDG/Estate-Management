from django.urls import path
from .views import *

urlpatterns = [
    path("A/<str:pk>/", agentsDashboard, name='dashboard-A'),
]
