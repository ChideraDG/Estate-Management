from django.urls import path
from .bo_view import bo_tenant_communications, search_clients, bo_chat, search_chats
from .tenant_view import tenant_communications, tenant_chat


urlpatterns = [
    # Building Owner Views
    path('search_clients/', search_clients, name='search_clients'),
    path('search_chats/', search_chats, name='search_chats'),
    path("bo/<pk>/communications/", bo_tenant_communications, name="bo-comms"),
    path("bo/<pk>/communications/<tenant_id>/", bo_chat, name='bo-chat'),

    # Tenant Views
    path("tenant/<pk>/communications", tenant_communications, name="tenant-comms"),
    path("tenant/<pk>/communications/<bo_id>/", tenant_chat, name="tenant-chat"),
]