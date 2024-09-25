from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from locations.models import Country, State
from users.views import greet_client, get_activity
from finances.models import Receipt
from .models import BuildingOwner
from .forms import BuildingOwnerForm


@login_required(login_url='login')
def building_owner_profile(request, pk):
    profile = request.user.profile.building_owner
    countries = Country.objects.all()

    if request.method == 'POST':
        form = BuildingOwnerForm(request.POST, request.FILES, instance=profile, request=request)

        if form.is_valid():
            instance = form.save(commit=False)
            old_instance = BuildingOwner.objects.get(user=profile.user.id)

            instance.building_owner_name = instance.building_owner_name.strip().title() if instance.building_owner_name else None

            # Track changes
            changes = []
            for field in form.changed_data:
                original_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                if original_value != new_value:
                    changes.append(field)
                
            instance.save()

            if changes:
                messages.success(request, 'Profile Updated!')
    else:
        form = BuildingOwnerForm(instance=profile)

    menu = 'user-management'
    s_menu = 'bo-profile'
    
    context = {
        's_menu': s_menu,
        'menu': menu,
        'profile': profile,
        'form': form, 
        'countries': countries, 
    }
    return render(request, 'building_owners/BuildingOwner.html', context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def building_owner_dashboard(request, pk):
    menu = 'building-owner-dashboard'
    greeting = greet_client() 
    no_of_houses = request.user.profile.building_owner.houses.all().count()

    activities, activities_time = get_activity(request)

    context = {
        'username': pk,
        'menu': menu,
        'greeting': greeting,
        'no_of_houses': no_of_houses,
        'activities': activities,
        'activities_time': activities_time,
    }
    return render(request, "building_owners/BO_dashboard.html", context)

@login_required(login_url='login')
def view_connections(request, pk):
    menu = 'user-management'
    s_menu = request.GET.get('s_menu', 'personal-profile')
    user_type = request.user.profile.designation
    labels = {
        "building_owner": 'BO',
        "agent": 'A',
        "buyer": 'B',
        "company": 'C',
        "tenant": 'T'
    }

    context = {
        's_menu': s_menu,
        'menu': menu,
        'type': labels.get(user_type)
    }
    return render(request, "building_owners/view_connections.html", context)

@login_required(login_url='login')
def rent_payment_history(request, pk):
    payments = Receipt.objects.filter(payment__lease__tenant__building_owner=request.user.profile.building_owner).order_by("-generated_on")
    context = {
        "menu": "fns",
        "s_menu": "rc",
        "payments": payments,
    }
    return render(request, "building_owners/rent_payment_history.html", context)
