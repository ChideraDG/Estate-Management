from django.urls import path
from .views import agentsDashboard, view_connections, agent_profile

urlpatterns = [
    path("A/<str:pk>/", agentsDashboard, name='dashboard-A'),
    path("A/<str:pk>/view-connections", view_connections, name="a-view-connections"),
    path('A/<str:pk>/a-profile/', agent_profile, name='view-agent'),
]
