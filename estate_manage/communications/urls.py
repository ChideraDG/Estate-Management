from django.urls import path
from .bo_views import bo_tenant_communications, search_clients, bo_chat, search_chats


urlpatterns = [
    path('search_clients/', search_clients, name='search_clients'),
    path('search_chats/', search_chats, name='search_chats'),
    path("bo/<pk>/communications/", bo_tenant_communications, name="bo-comms"),
    path("bo/<pk>/communications/<tenant_id>/", bo_chat, name='bo-chat'),
]