"""
Django URL Configuration

This file defines the URL patterns for the application.

Examples:
    - `/`: Homepage
    - `/register/`: User registration page
    - `/login/`: User login page
    - `/logout/`: User logout page
    - `/delete-user/`: Delete user account page
    - `/dashboard/`: User dashboard page
    - `/property-single/`: Single property details page
    - `/property-grid/`: Property grid listing page
    - `/blog-single/`: Single blog post page
    - `/agents-grid/`: Agents grid listing page
    - `/agent-single/`: Single agent details page
    - `/about/`: About us page
    - `/blog/`: Blog listing page
    - `/contact-us/`: Contact us page

"""

from django.urls import path
from .views import (home, userRegister, userLogin, userLogout,
                    dashboard, property_grid, property_single,
                    blog_single, agents_grid, agent_single, about,
                    blog, contact_us, userDelete, userView, userUpdate)

urlpatterns = [
    path("", home, name='home'),
    path("register/", userRegister, name='register'),
    path("login/", userLogin, name='login'),
    path("logout/", userLogout, name='logout'),
    path("delete-user/", userDelete, name='delete-user'),
    path("dashboard/", dashboard, name='dashboard'),
    path("property-single/", property_single, name='property-single'),
    path("property-grid/", property_grid, name='property-grid'),
    path("blog-single/", blog_single, name='blog-single'),
    path("agents-grid/", agents_grid, name='agents-grid'),
    path("agent-single/", agent_single, name='agent-single'),
    path("about/", about, name='about'),
    path("blog/", blog, name='blog'),
    path("contact-us/", contact_us, name='contact-us'),
    path("dashboard/<str:pk>/view-profile/", userView, name="view-user-profile"),
    path("dashboard/<str:pk>/update-profile/", userUpdate, name="update-user-profile")
]