from urllib.parse import urlencode
from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import House, Photo
from.forms import HouseForm, HouseFilterForm
from .utils import paginateHouses


@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def building_owner_houses(request, pk):
    """
    Manage and display houses for a building owner.

    This view retrieves houses related to the building owner's profile, filters them, 
    and paginates the results. It also handles form submissions for adding new houses, 
    including managing Many-to-Many relationships for utilities and features and 
    uploading house images.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing user data and GET/POST parameters.
    pk : int
        The primary key of the building owner's profile.

    Returns
    -------
    HttpResponse
        Renders the 'BO_houses.html' template with the context, including 
        filtered house data, form data, and pagination.

    Notes
    -----
    - The function handles both GET and POST requests.
    - On GET, it filters and paginates houses, then renders the page.
    - On POST, it processes the form for creating a new house, along with 
      managing the many-to-many fields for utilities and features and saving 
      images related to the house.
    """
    # Get the building owner's profile from the current user's profile.
    profile = request.user.profile.building_owners

    # Filter houses using the filterHouses function and get the query string for filtering.
    houses, query_string = filterHouses(request)

    # Get the current menu or default to 'all' if not provided.
    menu = request.GET.get('menu', 'all')

    # Get the reset filter URL or default to '/' if not provided.
    reset_filter = request.GET.get('reset_filter', '/')

    # Set the active menu and sub-menu for UI highlighting.
    active_menu = 'houses-management'
    active_sub_menu = 'house-profiles'

    # Retrieve all countries (presumably for filtering options).
    countries = Country.objects.all()

    # Filter houses by their occupancy status.
    occupied_houses = houses.filter(occupancy_status="occupied")
    vacant_houses = houses.filter(occupancy_status="vacant")

    # Check if there are any houses, occupied houses, or vacant houses.
    exist = [houses.exists(), occupied_houses.exists(), vacant_houses.exists()]

    # Paginate the houses, showing 6 houses per page.
    custom_range, houses = paginateHouses(request, houses, 6)
    oh_custom_range, occupied_houses = paginateHouses(request, occupied_houses, 6)
    vh_custom_range, vacant_houses = paginateHouses(request, vacant_houses, 6)

    # If the request method is POST, process the form for adding a new house.
    if request.method == "POST":
        # Instantiate the HouseForm with POST data.
        form = HouseForm(request.POST)

        # Get the list of images uploaded with the form.
        images = request.FILES.getlist('images')

        # Check if the form is valid.
        if form.is_valid():
            # Create a model instance from the form but don't save it yet.
            instance = form.save(commit=False)
            # Assign the building owner to the house instance.
            instance.building_owner = profile

            # Save the house instance to the database.
            instance.save()

            # Access the Many-to-Many Table for utilities and save selected utilities.
            HouseUtilities = House.utilities.through
            for utility in request.POST.getlist('utilities'):
                HouseUtilities.objects.create(house_id=instance.id, utility_id=utility)

            # Access the Many-to-Many Table for features and save selected features.
            HouseFeatures = House.features.through
            for feature in request.POST.getlist('features'):
                HouseFeatures.objects.create(house_id=instance.id, feature_id=feature)

            # Save each uploaded image to the Photo model with the associated house.
            for image in images:
                Photo.objects.create(
                    image=image,
                    house=instance,
                )
            
            # Redirect to the same view after successful form submission.
            return redirect('bo-houses', pk=profile)

    # If the request method is GET, instantiate an empty HouseForm.
    else:
        form = HouseForm()

    # Prepare the context to be passed to the template.
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
        'filter_form': HouseFilterForm(),
        'exist': exist,
        'reset_filter': reset_filter,
        'query_string': query_string,
    }

    # Render the 'BO_houses.html' template with the prepared context.
    return render(request, "houses/BO_houses.html", context)


def filterHouses(request):
    """
    Filter houses based on the current user's profile and the provided form data.

    This function retrieves all houses related to the current user's profile 
    and filters them according to the criteria provided in the HouseFilterForm. 
    It handles both direct and lookup-based filtering, including filtering for 
    ForeignKey and ManyToManyField relationships.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing the user and GET parameters for filtering.

    Returns
    -------
    tuple
        A tuple containing:
        - QuerySet : The filtered houses based on the applied criteria.
        - str : The generated query string from the GET parameters.
        
    Notes
    -----
    - This function handles country and state filters using ForeignKey lookups.
    - For other fields, it directly maps form fields to model field filters.
    - ManyToManyField and ForeignKey fields with multiple options are handled 
      using the `__in` lookup.
    """
    
    # Get all houses related to the current user's profile
    houses = request.user.profile.building_owners.houses.all()
    form = HouseFilterForm(request.GET)

    if form.is_valid():
        filters = {}

        # Handle country and state separately since they require lookups
        _country = form.cleaned_data.get('_country')
        _state = form.cleaned_data.get('_state')
        
        if _country:
            filters['country'] = Country.objects.filter(name=_country).first()
        if _state:
            filters['state'] = State.objects.filter(name=_state).first()

        # Define the fields that need direct filtering
        fields_to_filters = {
            'house_no': 'house_number',
            'house_address': 'address__icontains',
            'city': 'city__icontains',
            'number_of_apartments': 'number_of_apartments',
            'number_of_floors': 'number_of_floors',
            'garage_space': 'garage_space',
            'renovation_year': 'renovation_year',
            'condition': 'condition__icontains',
            'house_size_min': 'house_size__gte',
            'house_size_max': 'house_size__lte',
            'sale_price_min': 'sale_price__gte',
            'sale_price_max': 'sale_price__lte',
            'rent_price_min': 'rent_price__gte',
            'rent_price_max': 'rent_price__lte',
            'yard_size_min': 'yard_size__gte',
            'yard_size_max': 'yard_size__lte',
        }

        # Loop through the fields and add non-empty filters
        for field, filter_name in fields_to_filters.items():
            value = form.cleaned_data.get(field)
            if value:
                filters[filter_name] = value

        # Handle ManyToManyField or ForeignKey fields with __in lookup
        if form.cleaned_data.get('features'):
            filters['features__in'] = form.cleaned_data['features']
        if form.cleaned_data.get('utilities'):
            filters['utilities__in'] = form.cleaned_data['utilities']

        # Apply the filters to the queryset
        houses = houses.filter(**filters)

        # Generate the query string for the current GET parameters
        cleaned_query_dict = {key: value for key, value in request.GET.items() if value}
        query_string = urlencode(cleaned_query_dict)

    return houses, query_string

@login_required(login_url='login')
def house_details(request, pk, house_id):
    house = request.user.profile.building_owners.houses.get(id=house_id)
    active_menu = 'houses-management'
    active_sub_menu = 'house-profiles'

    if request.method == "POST":
        form = HouseForm(request.POST, instance=house)
        images = request.FILES.getlist('images')

        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            instance.save()

            HouseUtilities = House.utilities.through  # Accessing a Many-to-Many Table of Utility
            #  Clear all existing utilities for this house
            instance.utilities.clear()
            for utility in request.POST.getlist('utilities'):
                HouseUtilities.objects.get_or_create(house_id=instance.id, utility_id=utility)

            HouseFeatures = House.features.through  # Accessing a Many-to-Many Table of Feature
            #  Clear all existing utilities for this house
            instance.features.clear()
            for feature in request.POST.getlist('features'):
                HouseFeatures.objects.get_or_create(house_id=instance.id, feature_id=feature)

            for image in images:
                Photo.objects.get_or_create(
                    image=image,
                    house=instance,
                )
            
            return redirect('house-details', pk=house.building_owner, house_id=house.id)
    else:
        form = HouseForm(instance=house)

    context = {
        'house': house,
        'form': form,
        'active_menu': active_menu,
        'active_sub_menu': active_sub_menu,
    }
    return render(request, "houses/BO_house_details.html", context)

@login_required(login_url='login')
def delete_house(request, pk):
    house = request.user.profile.building_owners.houses.get(id=pk)
    house.delete()

    return redirect('bo-houses', pk=request.user.profile)