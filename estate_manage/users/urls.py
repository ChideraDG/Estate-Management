from django.urls import path
from .views import *
from estates.views import *

urlpatterns = [
    path("", welcome, name='welcome'),
    path("register/", userRegister, name='register'),
    path("login/", userLogin, name='login'),
    path("logout/", userLogout, name='logout'),
    path("welcome/", test, name='welcome'),
]
