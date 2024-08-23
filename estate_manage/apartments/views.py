from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from houses.models import House
from .models import Apartment, Photo
from .forms import ApartmentForm


def createApartment(request):
    # countries = Country.objects.all()
    form = ApartmentForm()

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('apartment-home')

    context = {'form': form,}
    return render(request, 'apartments/apartmentReg.html', context)

def updateApartment(request, pk):
    profile = Apartment.objects.get(id=pk)
    # countries = Country.objects.all()
    form = ApartmentForm(instance=profile)

    if request.method == "POST":
        form = ApartmentForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('apartment-home')

    context = {'form': form, 'profile': profile}
    return render(request, 'apartments/apartmentReg.html', context)

def deleteApartment(request, pk):
    profile = Apartment.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('apartment-home')
    context = {'obj': profile}
    return render(request, 'apartments/deleteApartment.html', context)

@login_required(login_url='login')
def house_apartments(request, pk, type):
    active_menu = 'apartments-management'
    active_sub_menu = 'apartment-profiles'
    if type == "bo":
        houses = request.user.profile.building_owners.houses.all()

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
        'tenant': "tenants/T_dashboard.html"
    }
    context = {
        'active_menu': active_menu,
        'active_sub_menu': active_sub_menu,
        'houses': houses,
        'type': type,
        'template_routes': template_routes.get(request.user.profile.designation),
    }
    return render(request, 'apartments/house_apartments.html', context)

@login_required(login_url='login')
def view_apartments(request, type, pk, house_id):
    active_menu = request.GET.get('active_menu', '/')
    active_sub_menu = request.GET.get('active_sub_menu', '/')
    menu = request.GET.get('menu', 'all')
    house = House.objects.get(id=house_id)
    apartments = house.apartments.all()
    occupied_apartments = [ apartment for apartment in apartments if apartment.is_occupied ]
    vacant_apartments = [ apartment for apartment in apartments if not apartment.is_occupied ]
    exist = [apartments.exists(), len(occupied_apartments), len(vacant_apartments)]

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request=request)
        # Get the list of images uploaded with the form.
        images = request.FILES.getlist('images')

        if form.is_valid():
            instance = form.save(commit=False)
            instance.house = house
            try:
                instance.save()
            except IntegrityError:
                messages.error(request, f"Apartment {request.POST['apartment_number']} already exists in this house.")

            for image in images:
                Photo.objects.create(
                    image=image,
                    apartment=instance,
                    description=f'{instance}'
                )

            return redirect('view-apartments', type=type, pk=pk, house_id=house_id)
    else:
        form = ApartmentForm()

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
        'tenant': "tenants/T_dashboard.html"
    }
    context = {
        'template_routes': template_routes.get(request.user.profile.designation),
        'active_menu': active_menu,
        'active_sub_menu': active_sub_menu,
        'house': house,
        'apartments': apartments,
        'type': type,
        'form': form,
        'menu': menu,
        'occupied_apartments': occupied_apartments,
        'vacant_apartments': vacant_apartments,
        'exist': exist,
    }
    return render(request, 'apartments/view_apartments.html', context)