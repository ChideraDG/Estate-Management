from django.urls import path
from .views import (tracking, request_submission, service_provider)

urlpatterns = [
    path('tenant/<pk>/tracking/', tracking, name='tracking'),
    path('tenant/<pk>/log-request/', request_submission, name='log_request'),
    path('tenant/<pk>/service_provider/', service_provider, name='service_provider'),
]