from django.urls import path
from .views import (home, userRegister, userLogin, userLogout,
                    dashboard, property_grid, property_single,
                    blog_single, agents_grid, agent_single, about,
                    blog, contact_us, userDelete)

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
]
