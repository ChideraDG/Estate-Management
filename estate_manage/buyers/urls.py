from django.urls import path
from .views import *

urlpatterns = [
    path('home/', buyerHome, name='buyer-home'),
    path('get_states/', get_states, name='get-states'),
    path('create/', createBuyer, name='create-buyer'),
    path('update/<str:pk>/', updateBuyer, name='update-buyer'),
    path('view/<str:pk>/', viewBuyer, name='view-buyer'),
    path('delete/<str:pk>/', deleteBuyer, name='delete-buyer'),
    path('<str:pk>/', buyerDashboard, name='B_dashboard'),
]
