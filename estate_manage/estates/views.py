from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .forms import ProfileForm
from company.models import Profile


def createProfile(request):
    form = ProfileForm()  # Initialize an empty ProfileForm.

    if request.method == "POST":  # Check if the request method is POST.
        form = ProfileForm(request.POST, request.FILES)  # Populate the form with POST data and uploaded files.
        if form.is_valid():  # Check if the form is valid.
            images = request.FILES.getlist('_images')  # Get the list of uploaded images from the form field named '_images'.
            image_paths = []  # Initialize an empty list to store the paths of saved images.

            for image in images:  # Iterate through each uploaded image.
                # Save each image to the 'estate-pics/' directory and store its path in the 'path' variable.
                path = default_storage.save('estate-pics/' + image.name, ContentFile(image.read()))
                image_paths.append(path)  # Append the saved image path to the image_paths list.

            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            instance.estate_image = image_paths  # Set the estate_image field of the instance to the list of image paths.
            instance.save()  # Save the instance to the database.

            return redirect('welcome')  # Redirect the user to the 'welcome' page after successful form submission.

    context = {'form': form}  # Create a context dictionary with the form.
    return render(request, 'estates/your.html', context)  # Render the 'estates/your.html' template with the context.
