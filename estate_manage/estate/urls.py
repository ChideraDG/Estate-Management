from django.urls import path
from .views import *

urlpatterns = [
    path("", welcome, name='welcome'),
    path("reg/", userRegister, name='reg'),
    path("login/", userLogin, name='login'),
    path("logout/", userLogout, name='logout'),
    path("welcome/", test, name='welcome'),
]
