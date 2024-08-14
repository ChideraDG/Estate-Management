from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from . models import BuildingOwner
from . forms import BuildingOwnerForm
from locations.models import Country, State


@login_required(login_url='login')
def updateProfile(request, pk):
    profile = request.user.profile.building_owners
    countries = Country.objects.all()
    form = BuildingOwnerForm(instance=profile)

    if request.method == 'POST':
        form = BuildingOwnerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            if instance.building_owner_name:
                instance.building_owner_name = instance.building_owner_name.strip().title()
            instance.save()
            messages.success(request, 'Profile updated successfully')

            return redirect('view-building-owner', pk=instance.user)
        
    context = {'form': form, 'countries': countries, 'profile':profile}
    return render (request, 'building_owners/updateBuildingOwner.html', context)

@login_required(login_url='login')
def viewProfile(request, pk):
    profile = request.user.profile.building_owners
    context = {'profile': profile}
    return render(request, 'building_owners/viewBuildingOwner.html', context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def buildingOwnerDashboard(request, pk):
    context = {'username': pk}
    return render(request, "building_owners/BO_dashboard.html", context)
