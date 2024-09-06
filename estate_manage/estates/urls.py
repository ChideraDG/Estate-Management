from django.urls import path
from .views import (get_states, estates)

urlpatterns = [
    path('get-states', get_states, name='get-states'),
     path('<str:type>/<str:pk>/estates/', estates, name='estates'),
]
