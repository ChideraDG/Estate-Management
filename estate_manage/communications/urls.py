from django.urls import path
from .views import bo_tenant_communications, search_clients, bo_chat


urlpatterns = [
    path('search_clients/', search_clients, name='search_clients'),
    path("bo/<pk>/communications/", bo_tenant_communications, name="bo-comms"),
    path("bo/<pk>/communications/<tenant_id>/", bo_chat, name='bo-chat'),
]