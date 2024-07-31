from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("register/", userRegister, name='register'),
    path("login/", userLogin, name='login'),
    path("logout/", userLogout, name='logout'),
]
