from django.urls import path
from .views import (notifications)

urlpatterns = [
    path('<type>/<pk>/notifications/', notifications, name='notify'),
]