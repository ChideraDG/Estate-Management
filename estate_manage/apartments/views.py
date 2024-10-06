from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib import messages
from houses.models import House
from .utils import paginateApartments
from .models import Apartment, Photo
from .forms import ApartmentForm, ApartmentFilterForm


@login_required(login_url='login')
def get_apartments(request):
    house_id = request.GET.get('house_id')
    apartments = Apartment.objects.filter(house=house_id)
    apartments_list = [{
        'id': apartment.id,
        'apartment_number': apartment.apartment_number, 
        'floor_number': apartment.floor_number
        } for apartment in apartments if not apartment.is_occupied
    ]
    return JsonResponse(apartments_list, safe=False)

@login_required(login_url='login')
def house_apartments(request, pk, type):
    menu = 'a-m'
    s_menu = 'a-p'
    if type == "bo":
        houses = request.user.profile.building_owner.houses.all()

    elif type == 'c':
        houses = request.user.profile.companies.houses.all()

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
        'tenant': "tenants/T_dashboard.html",
        'company': 'companies/C_dashboard.html'
    }
    context = {
        'menu': menu,
        's_menu': s_menu,
        'houses': houses,
        'type': type,
        'template_routes': template_routes.get(request.user.profile.designation),
    }
    return render(request, 'apartments/house_apartments.html', context)

@login_required(login_url='login')
def view_apartments(request, type, pk, house_id):
    menu = request.GET.get('menu', 'a-m')
    s_menu = request.GET.get('s_menu', 'a-p')
    i_menu = request.GET.get('i_menu', 'all')
    reset_filter = request.GET.get('reset_filter', '/')
    house = House.objects.get(id=house_id)
    apartments, query_string = filterApartments(request, house)
    total_apartment = apartments.count
    occupied_apartments = apartments.filter(is_occupied=1)
    vacant_apartments = apartments.filter(is_occupied=0)
    exist = [apartments.exists(), occupied_apartments.exists(), len(vacant_apartments)]
    custom_range, apartments = paginateApartments(request, apartments, 6)
    oa_custom_range, occupied_apartments = paginateApartments(request, occupied_apartments, 6)
    va_custom_range, vacant_apartments = paginateApartments(request, vacant_apartments, 6)
    filter_form = ApartmentFilterForm()

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
        'menu': menu,
        's_menu': s_menu,
        'house': house,
        'apartments': apartments,
        'type': type,
        'form': form,
        'i_menu': i_menu,
        'occupied_apartments': occupied_apartments,
        'vacant_apartments': vacant_apartments,
        'exist': exist,
        'oa_custom_range': oa_custom_range,
        'va_custom_range': va_custom_range,
        'custom_range': custom_range,
        'filter_form': filter_form,
        'query_string': query_string,
        'reset_filter': reset_filter,
        'house_id': house_id,
        'total_apartment': total_apartment,
    }
    return render(request, 'apartments/view_apartments.html', context)


def filterApartments(request, house):
    apartments = house.apartments.all()
    form = ApartmentFilterForm(request.GET, request=request)

    if form.is_valid():
        filters = {}

        # Define the fields that need direct filtering
        fields_to_filters = {
            'apartment_number': 'apartment_number__icontains',
            'floor_number': 'floor_number',
            'number_of_bedrooms': 'number_of_bedrooms',
            'number_of_bathrooms': 'number_of_bathrooms',
            'square_feet_min': 'square_feet__gte',
            'square_feet_max': 'square_feet__lte',
            'rent_price_min': 'rent_price__gte',
            'rent_price_max': 'rent_price__lte',
            'sale_price_min': 'sale_price__gte',
            'sale_price_max': 'sale_price__lte',
            'number_of_rooms': 'number_of_rooms',
            'kitchen_type': 'kitchen_type',
            'flooring_type': 'flooring_type',
            'heating_system': 'heating_system',
            'security_deposit': 'security_deposit__gte',
            'maintenance_fee': 'maintenance_fee__gte',
            'last_renovation_year': 'last_renovation_year',
            'condition': 'condition__icontains',
        }

        # Loop through the fields and add non-empty filters
        for field, filter_name in fields_to_filters.items():
            value = form.cleaned_data.get(field)
            if value:
                filters[filter_name] = value

        # Apply the filters to the queryset
        apartments = apartments.filter(**filters)

        # Generate the query string for the current GET parameters
        cleaned_query_dict = {key: value for key, value in request.GET.items() if value}
        query_string = urlencode(cleaned_query_dict)
    else:
        query_string = ""

    return apartments, query_string


@login_required(login_url='login')
def apartment_details(request, type, pk, house_id, apartment_number):
    house = House.objects.get(id=house_id)
    apartment = house.apartments.get(apartment_number=apartment_number)
    menu = request.GET.get('menu', 'a-m')
    s_menu = request.GET.get('s_menu', 'a-p')

    if request.method == "POST":
        form = ApartmentForm(request.POST, instance=apartment, request=request)
        images = request.FILES.getlist('images')

        if form.is_valid():
            instance = form.save(commit=False)
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

            return redirect('apartment-details', type, pk, house_id, instance.apartment_number)
    else:
        form = ApartmentForm(instance=apartment)

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
        'tenant': "tenants/T_dashboard.html"
    }
    context = {
        'house': house,
        'house_id': house_id,
        'type': type,
        'apartment': apartment,
        'menu': menu,
        's_menu': s_menu,
        'template_routes': template_routes.get(request.user.profile.designation),
        'form': form,
    }
    return render(request, 'apartments/apartment_details.html', context)

@login_required(login_url='login')
def delete_apartment(request, pk):
    user = request.user.profile.designation
    apartment = Apartment.objects.get(id=pk)
    house = apartment.house
    apartment.delete()

    designation_type = {
        'building_owner': "bo",
        'tenant': "T"
    }
    return redirect('view-apartments', designation_type.get(user), request.user.profile, house.id)