from django.urls import path
from .views import *

urlpatterns = [
    path("<str:pk>/", agentsDashboard, name='A_dashboard'),
]
