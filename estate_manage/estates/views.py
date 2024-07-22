from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Estate


def createProfile(request):
    form = ProfileForm()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('_images')  # Get the list of uploaded images from the form field named '_images'.
            image_paths = []  # Initialize an empty list to store the paths of saved images.

            for image in images:  # Iterate through each uploaded image.
                # Save each image to the 'estate-pics/' directory and store its path in the 'path' variable.
                path = default_storage.save('estate-pics/' + image.name, ContentFile(image.read()))
                image_paths.append(path)  # Append the saved image path to the image_paths list.

            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            instance.estate_image = image_paths  # Set the estate_image field of the instance to the list of image paths.

            instance.save()

            ProfileAmenities = Estate.amenities.through  # Accessing a Many-to-Many Table of Amenities
            for amenity in request.POST.getlist('amenities'):
                ProfileAmenities.objects.create(profile_id=instance.id, amenity_id=amenity)

            ProfileSecurityFeatures = Estate.security_features.through  # Accessing a Many-to-Many Table of Securities
            for security_features in request.POST.getlist('security_features'):
                ProfileSecurityFeatures.objects.create(profile_id=instance.id, securityfeatures_id=security_features)

            ProfileUtilities = Estate.utilities.through  # Accessing a Many-to-Many Table of Utility
            for utility in request.POST.getlist('utilities'):
                ProfileUtilities.objects.create(profile_id=instance.id, utilities_id=utility)

            return redirect('welcome')

    context = {'form': form}
    return render(request, 'estates/your.html', context)

