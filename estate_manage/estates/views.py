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

    estates =  Estate.objects.all()
    total_estates = estates.count

    # Retrieve all countries (presumably for filtering options).
    countries = Country.objects.all()

    # Filter estates by their types
    residential_estates = estates.filter(estate_type="residential")
    commercial_estates = estates.filter(estate_type="commercial")
    mixed_use_estates = estates.filter(estate_type="mixed_use ")

    # Check if exists
    exist = [estates.exists(), residential_estates.exists(), commercial_estates.exists(), mixed_use_estates.exists()] 

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

