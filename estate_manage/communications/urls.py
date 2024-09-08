from django.urls import path
from .views import bo_tenant_communications


urlpatterns = [
    path("bo/<pk>/communications/", bo_tenant_communications, name="bo-comms")
]