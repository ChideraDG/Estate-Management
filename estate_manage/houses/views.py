from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from .models import House
from.forms import HouseForm


def houseHome(request):
    profiles = House.objects.all()
    context = {'profiles': profiles}
    return render(request, 'houses/houseHome.html', context)

def createHouse(request):
    countries = Country.objects.all()
    form = HouseForm()

    if request.method == "POST":
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.

            instance.save()

            HouseUtilities = House.utilities.through  # Accessing a Many-to-Many Table of Utility
            for utility in request.POST.getlist('utilities'):
                HouseUtilities.objects.create(house_id=instance.id, utility_id=utility)

            HouseFeatures = House.features.through  # Accessing a Many-to-Many Table of Utility
            for feature in request.POST.getlist('features'):
                HouseFeatures.objects.create(house_id=instance.id, feature_id=feature)

            return redirect('house-home')


    context = {'form': form, 'countries': countries}
    return render(request, 'houses/houseReg.html', context)

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
