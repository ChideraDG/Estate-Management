from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("register/", userRegister, name='register'),
    path("login/", userLogin, name='login'),
    path("logout/", userLogout, name='logout'),
    path("dashboard/", dashboard, name='dashboard'),
    path("property-single/", property_single, name='property-single'),
    path("property-grid/", property_grid, name='property-grid'),
    path("blog-single/", blog_single, name='blog-single')
]
