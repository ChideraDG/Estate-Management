from django.urls import path
from .tenants_views import (tracking, request_submission, service_provider_details)
from .bo_views import (requests, cancel_request, reopen_request, delete_request,
                       completed_request, assign_service_provider, service_provider)

urlpatterns = [
    # tenants work-order urls
    path('tenant/<pk>/tracking/', tracking, name='tracking'),
    path('tenant/<pk>/log-request/', request_submission, name='log_request'),
    path('tenant/<pk>/service_provider/<workorder_id>/details/', service_provider_details, name='service_provider_details'),

    # building owner requests urls
    path('bo/<pk>/maintenance/requests/', requests, name='requests'),
    path('cancel-request/<pk>/', cancel_request, name='cancel_request'),
    path('reopen-request/<pk>/', reopen_request, name='reopen_request'),
    path('delete-request/<pk>/', delete_request, name='delete_request'),
    path('completed-request/<pk>/', completed_request, name='completed_request'),
    path('bo/<pk>/maintenance/requests/service-provider/<workorder_id>/assign/', assign_service_provider, name='assign_service_provider'),
    path('bo/<pk>/maintenance/requests/service-provider/<workorder_id>/details/', service_provider, name='service_provider'),
]