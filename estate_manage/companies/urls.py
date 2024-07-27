from django.urls import path
from .views import *

urlpatterns = [
  path('create/', createCompany, name='create-company'),
  path('update/<str:pk>/', updateCompany, name='update-company'),
  path('home/', companyHome, name='company-home'),
  path('view/<str:pk>/', viewCompany, name='view-company'),
  path('delete/<str:pk>/', deleteCompany, name='delete-company'),
]
