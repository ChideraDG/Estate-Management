from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Estate


def createEstate(request):
    form = ProfileForm()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist(
                '_images')  # Get the list of uploaded images from the form field named '_images'.
            image_paths = []  # Initialize an empty list to store the paths of saved images.

            for image in images:  # Iterate through each uploaded image.
                # Save each image to the 'estate-pics/' directory and store its path in the 'path' variable.
                path = default_storage.save('estate-pics/' + image.name, ContentFile(image.read()))
                image_paths.append(path)  # Append the saved image path to the image_paths list.

            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            instance.estate_name = instance.estate_name.strip().title()
            instance.estate_location = instance.estate_location.strip().title()
            instance.estate_image = image_paths  # Set the estate_image field of the instance to the list of image paths

            instance.save()

            EstateAmenities = Estate.amenities.through  # Accessing a Many-to-Many Table of Amenities
            for amenity in request.POST.getlist('amenities'):
                EstateAmenities.objects.create(estate_id=instance.id, amenity_id=amenity)

            EstateSecurityFeatures = Estate.security_features.through  # Accessing a Many-to-Many Table of Securities
            for security_features in request.POST.getlist('security_features'):
                EstateSecurityFeatures.objects.create(estate_id=instance.id, securityfeatures_id=security_features)

            EstateUtilities = Estate.utilities.through  # Accessing a Many-to-Many Table of Utility
            for utility in request.POST.getlist('utilities'):
                EstateUtilities.objects.create(estate_id=instance.id, utility_id=utility)

            return redirect('home-estate')

    context = {'form': form}
    return render(request, 'estates/createEstate.html', context)


def homeEstate(request):
    profiles = Estate.objects.all()
    context = {'profiles': profiles}
    return render(request, 'estates/homeEstate.html', context)


def updateEstate(request, pk):
    profile = Estate.objects.get(id=pk)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            images = request.FILES.getlist('_images')
            image_paths = []

            for image in images:
                path = default_storage.save('estate-pics/' + image.name, ContentFile(image.read()))
                image_paths.append(path)

            instance = form.save(commit=False)
            instance.estate_image = image_paths
            instance.save()

            # Clear existing many-to-many relationships
            instance.amenities.clear()
            instance.security_features.clear()
            instance.utilities.clear()

            # Add new many-to-many relationships
            for amenity in request.POST.getlist('amenities'):
                instance.amenities.add(amenity)

            for security_feature in request.POST.getlist('security_features'):
                instance.security_features.add(security_feature)

            for utility in request.POST.getlist('utilities'):
                instance.utilities.add(utility)

            instance.save()

            return redirect('home-estate')

    context = {'form': form, 'profile': profile}
    return render(request, 'estates/createEstate.html', context)


def deleteEstate(request, pk):
    profile = Estate.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('home-estate')
    context = {'obj': profile}
    return render(request, 'estates/deleteEstate.html', context)


def viewEstate(request, pk):
    estate = Estate.objects.get(id=pk)
    context = {'estate': estate}
    return render(request, 'estates/viewEstate.html', context)
