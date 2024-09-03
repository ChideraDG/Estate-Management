from django.urls import path
from . import views

urlpatterns = [
    path('<type>/<pk>/agreements/', views.lease_agreements, name='agreements'),
]
