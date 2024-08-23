from django.shortcuts import render, redirect
from .models import Tenant
from .forms import TenantForm
from django.http import JsonResponse
from locations.models import Country, State
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='login')
def tenant_profile(request, pk):
    profile = request.user.profile.tenants
    countries = Country.objects.all()
    

    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            old_instance = Tenant.objects.get(user=profile.user.id)

            instance.first_name = instance.first_name.strip().title() if instance.first_name else None
            instance.last_name = instance.last_name.strip().title() if instance.last_name else None
            instance.emergency_contact_name = instance.emergency_contact_name.strip().title() if instance.emergency_contact_name else None

             # Track changes
            changes = []
            for field in form.changed_data:
                original_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                if original_value != new_value:
                    changes.append(field)

            instance.save()
            
            if changes:
                messages.success(request, 'Profile Updated!')
    else:
        form = TenantForm(instance=profile)

    active_menu = 'user-management'
    active_sub_menu = 't-profile'
        
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'profile': profile,
        'form': form, 
        'countries': countries
        }
    return render(request, 'tenants/tenant.html', context)

@login_required(login_url='login')
def view_connections(request, pk):
    active_menu = 'user-management'
    active_sub_menu = request.GET.get('active_sub_menu', 'personal-profile')

    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
    }
    return render(request, "tenants/view_connections.html", context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
    
@login_required(login_url='login')
def tenantDashboard(request, pk):
    active_menu = 'tenant-dashboard'

    context = {
        'username': pk, 
        'active_menu': active_menu,
        }
    return render(request, "tenants/T_dashboard.html", context)

