"""
URL patterns for company-related views.

This module defines the URL patterns for creating, updating, viewing, and deleting companies.

Examples:
    - To create a new company, go to `/create/`
    - To update an existing company with ID `123`, go to `/update/123/`
    - To view the company home page, go to `/home/`
    - To view a specific company with ID `123`, go to `/view/123/`
    - To delete a company with ID `123`, go to `/delete/123/`

Note:
    The `pk` parameter in the URL patterns is the primary key of the company instance.
"""

from django.urls import path
from .views import (companyDashboard, companyProfile, view_connections)

urlpatterns = [
    path('company/<str:pk>/c-profile/', companyProfile, name='view-company'),
    path('company/<str:pk>/view-connections/', view_connections, name='c-view-connections'),
    path('company/<str:pk>/', companyDashboard, name='dashboard-C'),
]
