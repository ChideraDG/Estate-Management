from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('users.urls')),
    path("estates/", include('estates.urls')),
    path("company/dashboard/", include('companies.urls')),
    path("", include('building_owners.urls')),
    path("", include('houses.urls')),
    path("", include('apartments.urls')),
    path("", include('tenants.urls')),
    path("", include('agents.urls')),
    path('buyer/dashboard/', include('buyers.urls')),
    path("", include('leaseAgreements.urls')),
    path("", include('communications.urls')),
    path("", include('finances.urls')),
    path("", include('maintenances.urls')),

    path("reset_password/", CustomPasswordResetView.as_view(template_name='reset_password.html'),
         name='reset_password'),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
         name='password_reset_done'),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(template_name='reset.html'),
         name='password_reset_confirm'),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name='reset_password_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)