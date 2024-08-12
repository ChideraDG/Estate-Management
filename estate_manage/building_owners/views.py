from django.shortcuts import render, redirect
from . models import BuildingOwner
from . forms import BuildingOwnerForm
from locations.models import Country, State
from django.http import JsonResponse


def buildingOwnersHome(request):
    profiles = BuildingOwner.objects.all()
    context = {'profiles': profiles}
    return render(request, 'building_owners/buildingOwnersHome.html', context)


def createProfile(request):
    countries = Country.objects.all()
    form = BuildingOwnerForm()

    if request.method == 'POST':
        form = BuildingOwnerForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            if instance.building_owner_name:
                instance.building_owner_name = instance.building_owner_name.strip().title()
            instance.save()
            return redirect('building-owner-home')

    context = {'form': form, 'countries': countries}
    return render (request, 'building_owners/buildingOwnerReg.html', context)

def updateProfile(request, pk):
    profile = BuildingOwner.objects.get(id=pk)
    countries = Country.objects.all()
    form = BuildingOwnerForm(instance=profile)

    if request.method == 'POST':
        form = BuildingOwnerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            if instance.building_owner_name:
                instance.building_owner_name = instance.building_owner_name.strip().title()
            instance.save()

            return redirect('building-owner-home')
        
    context = {'form': form, 'countries': countries, 'profile':profile}
    return render (request, 'building_owners/buildingOwnerReg.html', context)

def viewProfile(request, pk):
    profile = BuildingOwner.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'building_owners/viewOwner.html', context)

def deleteProfile(request, pk):
    profile = BuildingOwner.objects.get(id=pk)

    if request.method == 'POST':
        profile.delete()
        return redirect('building-owner-home')
    
    context = {'obj': profile}
    return render(request, 'building_owners/deleteOwner.html', context)

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
