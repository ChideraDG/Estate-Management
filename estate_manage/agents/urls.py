from django.urls import path
from .views import (agentsDashboard, view_connections, agent_profile,
                    agent_properties, agent_house_apartments)

urlpatterns = [
    path("A/<str:pk>/", agentsDashboard, name='dashboard-A'),
    path("A/<str:pk>/view-connections", view_connections, name="a-view-connections"),
    path('A/<str:pk>/a-profile/', agent_profile, name='view-agent'),
    path("A/<str:pk>/properties/", agent_properties, name='agent-properties'),
    path("A/<str:pk>/properties/<str:p_id>/", agent_house_apartments, name='agent-house-apartments')
]
