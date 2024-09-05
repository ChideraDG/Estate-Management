from django.urls import path
from .views import (get_states)

urlpatterns = [
    path('get-states', get_states, name='get-states')
]
