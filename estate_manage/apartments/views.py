from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Apartment
from.forms import ApartmentForm


def apartmentHome(request):
    profiles = Apartment.objects.all()
    context = {'profiles': profiles}
    return render(request, 'apartments/apartmentHome.html', context)

def createApartment(request):
    countries = Country.objects.all()
    form = ApartmentForm()

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('apartment-home')

    context = {'form': form, 'countries': countries}
    return render(request, 'apartments/apartmentReg.html', context)

def updateApartment(request, pk):
    profile = Apartment.objects.get(id=pk)
    countries = Country.objects.all()
    form = ApartmentForm(instance=profile)

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('apartment-home')

    context = {'form': form, 'countries': countries, 'profile': profile}
    return render(request, 'apartments/apartmentReg.html', context)

def viewApartment(request, pk):
    apartment = Apartment.objects.get(id=pk)
    context = {'apartment': apartment}
    return render(request, 'apartments/viewApartment.html', context)

def deleteApartment(request, pk):
    profile = Apartment.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('apartment-home')
    context = {'obj': profile}
    return render(request, 'apartments/deleteApartment.html', context)

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def building_owner_apartments(request, pk):
    active_menu = 'apartments-management'
    active_sub_menu = 'apartment-profiles'
    houses = request.user.profile.building_owners.houses.all()
    apartments = []
    for house in houses:
        apartments.extend(house.apartments.all())

    
    context = {
        'active_menu': active_menu,
        'active_sub_menu': active_sub_menu,
        'apartments': apartments,
        'houses': houses,
    }
    return render(request, 'apartments/BO_apartments.html', context)