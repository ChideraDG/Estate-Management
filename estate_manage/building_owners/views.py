from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import BuildingOwner
from .forms import BuildingOwnerForm, AddTenantForm
from locations.models import Country, State
from apartments.models import Apartment
from tenants.models import Tenant
from houses.models import House
from users.views import generate_username, generate_password


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

    active_menu = 'user-management'
    active_sub_menu = 'bo-profile'
    
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
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
def building_owner_dashboard(request, pk):
    active_menu = 'building-owner-dashboard'

    context = {
        'username': pk,
        'active_menu': active_menu,
    }
    return render(request, "building_owners/BO_dashboard.html", context)

@login_required(login_url='login')
def view_connections(request, pk):
    active_menu = 'user-management'
    active_sub_menu = request.GET.get('active_sub_menu', 'personal-profile')
    user_type = request.user.profile.designation
    labels = {
        "building_owner": 'BO',
        "agent": 'A',
        "buyer": 'B',
        "company": 'C',
        "tenant": 'T'
    }


    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'type': labels.get(user_type)
    }
    return render(request, "building_owners/view_connections.html", context)

@login_required(login_url='login')
def tenant_profiles(request, pk):
    active_menu = 'tenants-management'
    active_sub_menu = 'tenant-profiles'
    profile = request.user.profile.building_owner
    houses = profile.houses.all()
    tenants = profile.tenants.all()

    if request.method == 'POST':
        form = AddTenantForm(request.POST, building_owner=profile, request=request)
        
        if form.is_valid():
            print(request.POST)
            username = generate_username(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
            password = generate_password()
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'].lower(),
                password=password,
                first_name=form.cleaned_data['first_name'].title(),
                last_name='tenant'
            )

            user.last_name = form.cleaned_data['last_name'].title()
            user.save()
            messages.success(request, "Tenant Successfully Created. \nTenants details sent to your Inbox")

            email = profile.contact_email
            subject = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} Profile Created"
            message = f'''
Welcome to EstateManage!

We are thrilled to assist in making your tenant's stay a comfortable and enjoyable experience. 
Below are their login details for seamless access:

Username: {username}
Password: {password}
Feel free to reach out if you need any assistance.

Warm regards,
The EstateManage Team
'''
            send_mail(from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email],
                      subject=subject,
                      message=message,
                      fail_silently=False)

            tenant = Tenant.objects.filter(user__username=username).first()
            tenant.building_owner = profile
            tenant.house = House.objects.filter(id=request.POST['_house']).first()
            tenant.apartment = Apartment.objects.filter(id=request.POST['_apartment']).first()
            tenant.first_name = request.POST['first_name']
            tenant.last_name = request.POST['last_name']
            tenant.email = request.POST['email']
            tenant.phone_number = request.POST['phone_number']
            tenant.country = House.objects.filter(id=request.POST['_house']).first().country
            tenant.state = House.objects.filter(id=request.POST['_house']).first().state
            tenant.city = House.objects.filter(id=request.POST['_house']).first().city
            tenant.move_in_date = request.POST['move_in_date']
            tenant.lease_start_date = request.POST['lease_start_date']
            tenant.lease_end_date = request.POST['lease_end_date']
            tenant.monthly_rent = request.POST['monthly_rent']
            tenant.deposit_amount = request.POST['deposit_amount']
            tenant.lease_term = request.POST['lease_term']
            tenant.payment_status = request.POST['payment_status']
            tenant.emergency_contact_name = request.POST['emergency_contact_name']
            tenant.emergency_contact_number = request.POST['emergency_contact_number']
            tenant.employment_status = request.POST['employment_status']
            tenant.occupation = request.POST['occupation']
            tenant.save()
        else:
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {errors}")
                
    else:
        form = AddTenantForm(building_owner=profile, request=request)

    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'tenants': tenants,
        'form': form,
        'houses': houses,
    }
    return render(request, "building_owners/bo_tenant_profiles.html", context)

