from django.urls import path
from .views import (rent_payment_portal)

urlpatterns = [
    path("tenant/<pk>/rent-payment/", rent_payment_portal, name="rent-payment"),
]