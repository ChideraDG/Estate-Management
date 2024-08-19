from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from .models import House, Photo
from.forms import HouseForm
from .utils import paginateHouses


def updateHouse(request, pk):
    countries = Country.objects.all()
    profile = House.objects.get(id=pk)
    form = HouseForm(instance=profile)

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            # Clear existing many-to-many relationships
            instance.utilities.clear()
            instance.features.clear()

            # Add new many to many relationship
            for utility in request.POST.getlist('utilities'):
                instance.utilities.add(utility)

            for feature in request.POST.getlist('features'):
                instance.features.add(feature)

            instance.save

            return redirect('house-home')

    context = {'form': form, 'countries': countries, 'profile': profile}
    return render(request, 'houses/houseReg.html', context)

def viewHouse(request, pk):
    house = House.objects.get(id=pk)
    context = {'house': house}
    return render(request, 'houses/viewhouse.html', context)

def deleteHouse(request, pk):
    profile = House.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('house-home')
    context = {'obj': profile}
    return render(request, 'houses/deleteHouse.html', context)

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def building_owner_houses(request, pk):
    profile = request.user.profile.building_owners
    houses =  request.user.profile.building_owners.houses.all()
    menu = request.GET.get('menu', '/')
    active_menu = 'houses-management'
    active_sub_menu = 'house-profiles'
    countries = Country.objects.all()
    occupied_houses  = request.user.profile.building_owners.houses.filter(occupancy_status="occupied")
    vacant_houses  = request.user.profile.building_owners.houses.filter(occupancy_status="vacant")
    custom_range, houses = paginateHouses(request, houses, 3)
    oh_custom_range, occupied_houses = paginateHouses(request, occupied_houses, 3)
    vh_custom_range, vacant_houses = paginateHouses(request, vacant_houses, 3)
    

    if request.method == "POST":
        form = HouseForm(request.POST)
        images = request.FILES.getlist('images')

        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            instance.building_owner = profile

            instance.save()

            HouseUtilities = House.utilities.through  # Accessing a Many-to-Many Table of Utility
            for utility in request.POST.getlist('utilities'):
                HouseUtilities.objects.create(house_id=instance.id, utility_id=utility)

            HouseFeatures = House.features.through  # Accessing a Many-to-Many Table of Utility
            for feature in request.POST.getlist('features'):
                HouseFeatures.objects.create(house_id=instance.id, feature_id=feature)

            for image in images:
                Photo.objects.create(
                    image=image,
                    house=instance,
                )
            
            return redirect('bo-houses', pk=profile)
    else:
        form = HouseForm()

    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'profile': profile,
        'houses': houses,
        'countries': countries,
        'form': form,
        'occupied_houses': occupied_houses,
        'vacant_houses': vacant_houses,
        'custom_range': custom_range,
        'oh_custom_range': oh_custom_range,
        'vh_custom_range': vh_custom_range,
        'menu': menu,
    }
    return render(request, "houses/BO_houses.html", context)