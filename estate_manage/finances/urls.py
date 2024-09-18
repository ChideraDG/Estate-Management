from django.urls import path
from .views import (rent_payment_portal, generate_rent_receipt)

urlpatterns = [
    path("tenant/<pk>/genarate_rent_receipt/", generate_rent_receipt, name="generate_rent_receipt"),
    path("tenant/<pk>/rent-payment/", rent_payment_portal, name="rent-payment"),
]
