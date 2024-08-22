from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import BuildingOwner
from .forms import BuildingOwnerForm
from locations.models import Country, State


@login_required(login_url='login')
def building_owner_profile(request, pk):
    profile = request.user.profile.building_owners
    countries = Country.objects.all()

    if request.method == 'POST':
        form = BuildingOwnerForm(request.POST, request.FILES, instance=profile, request=request)

        if form.is_valid():
            instance = form.save(commit=False)
            old_instance = BuildingOwner.objects.get(user=profile.user.id)

            instance.building_owner_name = instance.building_owner_name.strip().title() if instance.building_owner_name else None

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
        form = BuildingOwnerForm(instance=profile)

    active_menu = 'user-management'
    active_sub_menu = 'bo-profile'
    
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'profile': profile,
        'form': form, 
        'countries': countries, 
    }
    return render(request, 'building_owners/BuildingOwner.html', context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def building_owner_dashboard(request, pk):
    active_menu = 'building-owner-dashboard'

    context = {
        'username': pk,
        'active_menu': active_menu,
    }
    return render(request, "building_owners/BO_dashboard.html", context)

@login_required(login_url='login')
def view_connections(request, pk):
    active_menu = 'user-management'
    active_sub_menu = request.GET.get('active_sub_menu', 'personal-profile')
    user_type = request.user.profile.designation
    labels = {
        "building_owner": 'BO',
        "agent": 'A',
        "buyer": 'B',
        "company": 'C',
        "tenant": 'T'
    }


    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        "type": labels.get(user_type)
    }
    return render(request, "building_owners/view_connections.html", context)
