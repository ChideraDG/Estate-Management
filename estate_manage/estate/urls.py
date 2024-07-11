from django.urls import path
from .views import *

urlpatterns = [
    path("", welcome, name='welcome'),
    path("register/", register, name='register'),
    path("login/", login, name='login'),
    # path("test/", registerUser, name='test'),
]
