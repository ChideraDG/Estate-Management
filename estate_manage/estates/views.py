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

@login_required(login_url='login')
def estates(request, pk, type):
    if type == 'C':
        profile = request.user.profile.companies

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
    residential_estate = estates.filter(estate_type="residential")
    commercial_estate = estates.filter(estate_type="commercial")
    mixed_use_estate = estates.filter(estate_type="mixed_use ")

    # Check if exists
    exist = [estates.exists(), residential_estate.exists(), commercial_estate.exists(), mixed_use_estate.exists()] 

     # Paginate the estaes showing 6 estates per page.
    custom_range, estates = paginateHouses(request, estates, 6)
    re_custom_range, residential_estate = paginateHouses(request, residential_estate, 6)
    co_custom_range, commercial_estate = paginateHouses(request, commercial_estate, 6)
    mu_custom_range, mixed_use_estate = paginateHouses(request, mixed_use_estate, 6)

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
                instance.name = profile

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
               EstateSecurityFeatures.objects.create(estate_id=instance.id, security_feature_id=security_feature)

             # Save each uploaded image to the Photo model with the associated house.
            for image in images:
                Photo.objects.create(
                    image=image,
                    estate=instance,
                    description=f'{instance}'
                )
            
            # Redirect to the same view after successful form submission.
            return redirect('estates', pk=request.user.profile, type=type )
        else:
            non_field_errors = form.non_field_errors()
            if non_field_errors:
                for error in non_field_errors:
                    messages.error(request, error)

    # If the request method is GET, instantiate an empty HouseForm.
    else:
        form = EstateForm()

    # Prepare the context to be passed to the template.
    context = {
        's_menu': s_menu,
        'menu': menu,
        'profile': profile,
        'estates': estates,
        'countries': countries,
        'form': form,
        'exist': exist,
        'reset_filter': reset_filter,
        'query_string': query_string,
        'type': type,
        'residential_estate': residential_estate,
        'commercial_estate': commercial_estate,
        'mixed_use_estate': mixed_use_estate,
        'custom_range': custom_range,
        're_custom_range': re_custom_range,
        'co_custom_range': co_custom_range,
        'mu_custom_range': mu_custom_range,
        'i_menu': i_menu,
        'filter_form': EstateFilterForm(),
        'total_estates': total_estates,
        'add': add,
        }



    return render(request, 'estates/estates.html', context)

@login_required(login_url='login')
def FilterEstates(request):
    pass

def deleteEstate(request, pk):
    profile = Estate.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('home-estate')
    context = {'obj': profile}
    return render(request, 'estates/deleteEstate.html', context)



def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

