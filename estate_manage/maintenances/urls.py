from django.urls import path
from .tenants_views import (tracking, request_submission, service_provider)
from .bo_views import (requests)

urlpatterns = [
    # tenants work-order urls
    path('tenant/<pk>/tracking/', tracking, name='tracking'),
    path('tenant/<pk>/log-request/', request_submission, name='log_request'),
    path('tenant/<pk>/service_provider/', service_provider, name='service_provider'),

    # building owner requests urls
    path('bo/<pk>/maintenance/requests/', requests, name='requests'),
]