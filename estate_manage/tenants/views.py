from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from locations.models import Country, State
from houses.models import House
from apartments.models import Apartment
from users.views import generate_username, generate_password
from .models import Tenant
from .forms import TenantForm, TenantFilterForm, AddTenantForm
from .utils import paginateTenants


@login_required(login_url='login')
def tenant_profile(request, pk):
    profile = request.user.profile.tenant
    countries = Country.objects.all()
    

    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            old_instance = Tenant.objects.get(user=profile.user.id)

            instance.first_name = instance.first_name.strip().title() if instance.first_name else None
            instance.last_name = instance.last_name.strip().title() if instance.last_name else None
            instance.emergency_contact_name = instance.emergency_contact_name.strip().title() if instance.emergency_contact_name else None

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
        form = TenantForm(instance=profile)

    active_menu = 'user-management'
    active_sub_menu = 't-profile'
        
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'profile': profile,
        'form': form, 
        'countries': countries
        }
    return render(request, 'tenants/tenant.html', context)

@login_required(login_url='login')
def view_connections(request, pk):
    active_menu = 'user-management'
    active_sub_menu = request.GET.get('active_sub_menu', 'personal-profile')

    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
    }
    return render(request, "tenants/view_connections.html", context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
    
@login_required(login_url='login')
def tenantDashboard(request, pk):
    active_menu = 'tenant-dashboard'

    context = {
        'username': pk, 
        'active_menu': active_menu,
        }
    return render(request, "tenants/T_dashboard.html", context)


@login_required(login_url='login')
def tenants_profiles(request, pk, type):
    """
    Render the tenant profiles page for building owners or companies and handle form submissions for adding tenants.

    This view filters and paginates the tenants based on the current user's profile (building owner or company),
    displays the tenant profiles, and processes the form submission for adding a new tenant.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing user data, GET parameters, and POST data for form submission.
    pk : int
        The primary key of the user's profile.
    type : str
        The type of profile (e.g., 'building_owner' or 'company').

    Returns
    -------
    HttpResponse
        A rendered HTML page displaying the tenant profiles and a form to add tenants.
    """
    # Set active menu and submenu for the navigation bar
    active_menu = 'tenants-management'
    active_sub_menu = 'tenant-profiles'
    
    # Retrieve query parameters
    menu = request.GET.get('menu', 'all')
    reset_filter = request.GET.get('reset_filter', '/')
    
    # Determine the profile based on user designation (either building owner or company)
    if request.user.profile.designation == "building_owner":
        profile = request.user.profile.building_owner
    elif request.user.profile.designation == "company":
        profile = None  # Handle company case later (if needed)

    # Retrieve all houses related to the building owner
    houses = profile.houses.all()
    
    # Filter tenants based on the current request
    tenants, query_string = filterTenants(request)
    
    # Count total tenants and filter tenants by lease term
    total_tenants = tenants.count
    yearly_tenants = tenants.filter(lease_term="yearly")
    six_monthly_tenants = tenants.filter(lease_term="six_monthly")
    month_to_month_tenants = tenants.filter(lease_term="month_to_month")

    # Check if there are any tenants in each category
    exist = [tenants.exists(), yearly_tenants.exists(), six_monthly_tenants.exists(), month_to_month_tenants.exists()]

    # Paginate the tenants, displaying 6 tenants per page
    custom_range, tenants = paginateTenants(request, tenants, 6)
    yt_custom_range, yearly_tenants = paginateTenants(request, yearly_tenants, 6)
    smt_custom_range, six_monthly_tenants = paginateTenants(request, six_monthly_tenants, 6)
    m2mt_custom_range, month_to_month_tenants = paginateTenants(request, month_to_month_tenants, 6)

    # Process the form submission for adding a new tenant
    if request.method == 'POST':
        form = AddTenantForm(request.POST, building_owner=profile, request=request)
        
        if form.is_valid():
            # Generate a username and password for the new tenant
            username = generate_username(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
            password = generate_password()

            # Create a new user with the generated credentials
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'].lower(),
                password=password,
                first_name=form.cleaned_data['first_name'].title(),
                last_name='tenant' if type == "bo" else 'company'
            )
            user.last_name = form.cleaned_data['last_name'].title()
            user.save()

            # Display a success message and notify the building owner via email
            messages.success(request, "Tenant Successfully Created. \nTenant's details sent to your Inbox")

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
            send_mail(
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                subject=subject,
                message=message,
                fail_silently=False
            )

            # Update tenant details and associate the tenant with the house and apartment
            tenant = Tenant.objects.filter(user__username=username).first()
            if request.user.profile.designation == "building_owner":
                tenant.building_owner = profile
            tenant.house = House.objects.filter(id=request.POST['_house']).first()
            tenant.apartment = Apartment.objects.filter(id=request.POST['_apartment']).first()
            tenant.first_name = request.POST['first_name']
            tenant.last_name = request.POST['last_name']
            tenant.email = request.POST['email']
            tenant.phone_number = request.POST['phone_number']
            tenant.country = tenant.house.country
            tenant.state = tenant.house.state
            tenant.city = tenant.house.city
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

            # Clear the form by redirecting to the same page
            return redirect('tenants-profiles', pk=pk, type=type)
        else:
            # Print form errors for debugging purposes
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {errors}")
                
    else:
        # If the request is GET, initialize an empty form
        form = AddTenantForm(building_owner=profile, request=request)

    # Define the template route based on the user designation
    template_route = {
        'building_owner': "building_owners/BO_dashboard.html"
    }
    
    # Prepare the context to be passed to the template
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'tenants': tenants,
        'form': form,
        'houses': houses,
        'type': type,
        'menu': menu,
        'yearly_tenants': yearly_tenants,
        'six_monthly_tenants': six_monthly_tenants,
        'month_to_month_tenants': month_to_month_tenants,
        'filter_tenant': TenantFilterForm(),
        'template_route': template_route.get(request.user.profile.designation),
        'query_string': query_string,
        'reset_filter': reset_filter,
        'total_tenants': total_tenants,
        'custom_range': custom_range,
        'yt_custom_range': yt_custom_range,
        'smt_custom_range': smt_custom_range,
        'm2mt_custom_range': m2mt_custom_range,
        'exist': exist,
    }
    
    # Render the tenants_profiles.html template with the provided context
    return render(request, "tenants/tenants_profiles.html", context)

def filterTenants(request):
    """
    Filter tenants based on the current user's profile and the provided form data.

    This function retrieves all tenants related to the current user's profile
    and filters them according to the criteria provided in the TenantFilterForm.
    It handles direct and lookup-based filtering for ForeignKey relationships 
    and numeric range filters.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing the user and GET parameters for filtering.

    Returns
    -------
    tuple
        A tuple containing:
        - QuerySet : The filtered tenants based on the applied criteria.
        - str : The generated query string from the GET parameters.
        
    Notes
    -----
    - This function handles filtering based on tenant details like first name, 
      last name, email, and more, along with date and rent range filtering.
    - Handles ForeignKey relationships such as filtering tenants based on house.
    """
    
    if request.user.profile.designation == 'building_owner':
        # Get all tenants related to the current user's houses
        tenants = request.user.profile.building_owner.tenants.all()
    elif request.user.profile.designation == 'company':
        # Needs fixing: Assume company filters tenants related to their estates
        tenants = request.user.profile.company.tenants.all()
    else:
        tenants = Tenant.objects.none()

    form = TenantFilterForm(request.GET, request=request)
    if form.is_valid():
        filters = {}

        # Define the fields that need direct filtering
        fields_to_filters = {
            'first_name': 'first_name__icontains',
            'last_name': 'last_name__icontains',
            'email': 'email__icontains',
            '_house': 'house',
            'lease_start_date_min': 'lease_start_date__gte',
            'lease_start_date_max': 'lease_start_date__lte',
            'lease_end_date_min': 'lease_end_date__gte',
            'lease_end_date_max': 'lease_end_date__lte',
            'move_in_date_min': 'move_in_date__gte',
            'move_in_date_max': 'move_in_date__lte',
            'monthly_rent_min': 'monthly_rent__gte',
            'monthly_rent_max': 'monthly_rent__lte',
        }

        # Loop through the fields and add non-empty filters
        for field, filter_name in fields_to_filters.items():
            value = form.cleaned_data.get(field)
            if value:
                filters[filter_name] = value

        # Apply the filters to the queryset
        tenants = tenants.filter(**filters)

        # Generate the query string for the current GET parameters
        cleaned_query_dict = {key: value for key, value in request.GET.items() if value}
        query_string = urlencode(cleaned_query_dict)
    else:
        for field, errors in form.errors.items():
            print(f"Field: {field}, Errors: {errors}")
        query_string = ""

    return tenants, query_string