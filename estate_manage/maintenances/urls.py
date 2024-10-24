from django.urls import path
from .tenants_views import (tracking, request_submission, service_provider)
from .bo_views import (requests, cancel_request, reopen_request, delete_request,
                       completed_request)

urlpatterns = [
    # tenants work-order urls
    path('tenant/<pk>/tracking/', tracking, name='tracking'),
    path('tenant/<pk>/log-request/', request_submission, name='log_request'),
    path('tenant/<pk>/service_provider/', service_provider, name='service_provider'),

    # building owner requests urls
    path('bo/<pk>/maintenance/requests/', requests, name='requests'),
    path('cancel-request/<pk>/', cancel_request, name='cancel_request'),
    path('reopen-request/<pk>/', reopen_request, name='reopen_request'),
    path('delete-request/<pk>/', delete_request, name='delete_request'),
    path('completed-request/<pk>/', completed_request, name='completed_request'),
]