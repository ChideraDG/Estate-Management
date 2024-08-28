from django.urls import path
from .views import (agentsDashboard, view_connections, agent_profile,
                    agent_properties, agent_house_apartments, agent_house_apartment_details)

urlpatterns = [
    path("A/<str:pk>/", agentsDashboard, name='dashboard-A'),
    path("A/<str:pk>/view-connections", view_connections, name="a-view-connections"),
    path('A/<str:pk>/a-profile/', agent_profile, name='view-agent'),
    path("A/<str:pk>/properties/", agent_properties, name='agent-properties'),
    path("A/<str:pk>/properties/<str:house_id>/", agent_house_apartments, name='agent-house-apartments'),
    path("A/<str:pk>/properties/<str:house_id>/<str:apartment_no>/", agent_house_apartment_details, name='agent-house-apartment-details')
]
