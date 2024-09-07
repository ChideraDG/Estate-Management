from django.urls import path
from . import views

urlpatterns = [
    path('<type>/<pk>/agreements/', views.lease_agreements, name='agreements'),
    path('<type>/<pk>/agreements/<agreement_id>/', views.agreements_details, name='agreement-detail'),
    path('<type>/<pk>/agreements/<agreement_id>/update/', views.update_agreement, name='update-agreement'),
]
