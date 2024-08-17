from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .forms import BuildingOwnerForm
from locations.models import Country, State


@login_required(login_url='login')
def update_building_owner_profile(request, pk):
    profile = request.user.profile.building_owners
    countries = Country.objects.all()
    form = BuildingOwnerForm(instance=profile)

    if request.method == 'POST':
        form = BuildingOwnerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.building_owner_name = instance.building_owner_name.strip().title() if instance.building_owner_name else None
            instance.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('view-building-owner', pk=instance.user)

    active_menu = 'user-management'
    active_sub_menu = 'bo-profile'

    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'form': form, 
        'countries': countries, 
        'profile': profile
    }
    return render(request, 'building_owners/updateBuildingOwner.html', context)

@login_required(login_url='login')
def view_building_owner_profile(request, pk):
    profile = request.user.profile.building_owners

    active_menu = 'user-management'
    active_sub_menu = 'bo-profile'
    
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'profile': profile
    }
    return render(request, 'building_owners/viewBuildingOwner.html', context)

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

def view_connections(request, pk):
    active_menu = 'user-management'
    active_sub_menu = 'bo-profile'
    
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
    }
    return render(request, "building_owners/view_connections.html", context)
