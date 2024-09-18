from django.shortcuts import render, redirect
from urllib.parse import urlencode
from .forms import EstateForm, EstateFilterForm
from .models import Estate, Photo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from locations.models import Country, State
from django.http import JsonResponse
from urllib.parse import urlencode
from .utils import paginateEstates
from django.db import IntegrityError

@login_required(login_url='login')
def estates(request, pk, type):
    if type == 'c':
        profile = request.user.profile.companies

    # estates =  Estate.objects.all()
    estates, query_string = FilterEstates(request)
    total_estates = estates.count

    # Get the current menu or default to 'all' if not provided.
    i_menu = request.GET.get('i_menu', 'all')
    add = request.GET.get('add', 'all')

    # Get the reset filter URL or default to '/' if not provided.
    reset_filter = request.GET.get('reset_filter', '/')

    # Set the active menu and sub-menu for UI highlighting.
    menu = 'estates-management'
    s_menu = 'estate-profiles'


    # Retrieve all countries (presumably for filtering options).
    countries = Country.objects.all()

    # Filter estates by their types
    residential_estates = estates.filter(estate_type="residential")
    commercial_estates = estates.filter(estate_type="commercial")
    mixed_use_estates = estates.filter(estate_type="mixed_use ")

    # Check if exists
    exist = [estates.exists(), residential_estates.exists(), commercial_estates.exists(), mixed_use_estates.exists()] 

    custom_range, estates = paginateEstates(request, estates, 6)
    re_custom_range, residential_estates = paginateEstates(request, residential_estates, 6)
    co_custom_range, commercial_estates = paginateEstates(request, commercial_estates, 6)
    mu_custom_range, mixed_use_estates = paginateEstates(request, mixed_use_estates, 6)

    # If the request method is POST, process the form for adding a new estate.
    if request.method == "POST":
        form = EstateForm(request.POST)

         # Get the list of images uploaded with the form.
        images = request.FILES.getlist('images')

        # Check if the form is valid.
        if form.is_valid():
            # Create a model instance from the form but don't save it yet.
            instance = form.save(commit=False)

            if request.user.profile.designation == 'company':
                instance.company = profile

            # try:

            # Save the house instance to the database.
            instance.save()

            # Access the Many-to-Many Table for utilities and save selected utilities.
            EstateUtilities = Estate.utilities.through
            for utility in request.POST.getlist('utilities'):
                EstateUtilities.objects.create(estate_id=instance.id, utility_id=utility)

            # Access the Many-to-Many Table for amenities and save selected amenities.
            EstateAmenities = Estate.amenities.through
            for amenity in request.POST.getlist('amenities'):
                EstateAmenities.objects.create(estate_id=instance.id, amenity_id=amenity)

            # Access the Many-to-Many Table for utilities and save selected security features.
            EstateSecurityFeatures = Estate.security_features.through
            for security_feature in request.POST.getlist('security_features'):
                EstateSecurityFeatures.objects.create(estate_id=instance.id, securityfeatures_id=security_feature)

            # Save each uploaded image to the Photo model with the associated house.
            for image in images:
                Photo.objects.create(
                    image=image,
                    estate=instance,
                    description=f'{instance}'
                )
            
            # Redirect to the same view after successful form submission.
            return redirect('estates', pk=request.user.profile, type=type )

            # except IntegrityError:
                # Handle the error
                # messages.error(request, 'An estate with this name and address already exists.')
        else:
            non_field_errors = form.non_field_errors()
            if non_field_errors:
                for error in non_field_errors:
                    messages.error(request, error)

    # If the request method is GET, instantiate an empty HouseForm.
    else:
        form = EstateForm()


    context ={
        'profile': profile,
        'estates': estates,
        'form': form,
        'type': type,
        'exist': exist,
        'total_estates': total_estates,
        'residential_estates': residential_estates,
        'commercial_estates': commercial_estates,
        'mixed_use_estates': mixed_use_estates,
        'filter_form': EstateFilterForm(),
        'i_menu': i_menu,
        'reset_filter': reset_filter,
        'query_string': query_string,
        'add': add,
        's_menu': s_menu,
        'menu': menu,
        'countries': countries,
        'custom_range': custom_range,
        're_custom_range': re_custom_range,
        'co_custom_range': co_custom_range,
        'mu_custom_range': mu_custom_range,
    }
    return render(request, 'estates/estates.html', context)

def FilterEstates(request):
    if request.user.profile.designation == 'company':
        # Needs fixing
        print("User profile:", request.user.profile)
        print("User companies:", request.user.profile.companies)
        estates = Estate.objects.filter(company=request.user.profile.companies)
        print("Initial estates:", estates) 
    
    form = EstateFilterForm(request.GET, request=request)

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
            'estate_name': 'estate_name__icontains',  # Partial match for estate name
            'address': 'address__icontains',          # Partial match for estate address
            '_country': 'country',                    # Exact match for country (ForeignKey)
            '_state': 'state',                        # Exact match for state (ForeignKey)
            'min_number_of_houses': 'number_of_houses__gte',  # Greater than or equal to for minimum number of houses
            'max_number_of_houses': 'number_of_houses__lte',  # Less than or equal to for maximum number of houses
            'min_total_area_covered': 'total_area_covered__gte',  # Greater than or equal to for minimum total area covered
            'max_total_area_covered': 'total_area_covered__lte',  # Less than or equal to for maximum total area covered
            'min_land_area': 'land_area__gte',         # Greater than or equal to for minimum land area
            'max_land_area': 'land_area__lte',         # Less than or equal to for maximum land area
            'min_maintenance_cost': 'maintenance_cost__gte',  # Greater than or equal to for minimum maintenance cost
            'max_maintenance_cost': 'maintenance_cost__lte',  # Less than or equal to for maximum maintenance cost
            'city': 'city__icontains',                 # Partial match for city
            'construction_type': 'construction_type',  # Exact match for construction type
            'utilities': 'utilities__in',              # ManyToManyField for utilities (multiple options)
            'security_features': 'security_features__in',  # ManyToManyField for security features
            'amenities': 'amenities__in',              # ManyToManyField for amenities
        }

         # Loop through the fields and add non-empty filters
        for field, filter_name in fields_to_filters.items():
            value = form.cleaned_data.get(field)
            if value:
                filters[filter_name] = value

        # Handle ManyToManyField or ForeignKey fields with __in lookup
        if form.cleaned_data.get('security_features'):
            filters['security_features__in'] = form.cleaned_data['security_features']
        if form.cleaned_data.get('utilities'):
            filters['utilities__in'] = form.cleaned_data['utilities']
        if form.cleaned_data.get('amenities'):
            filters['amenities__in'] = form.cleaned_data['amenities']

         # Apply the filters to the queryset
        estates = estates.filter(**filters)

        # Generate the query string for the current GET parameters
        cleaned_query_dict = {key: value for key, value in request.GET.items() if value}
        query_string = urlencode(cleaned_query_dict)
    else:
        query_string = ""

    return estates, query_string

        


def deleteEstate(request, pk):
    pass


def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

