from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from locations.models import Country, State
from .models import Agent
from .forms import AgentForm


@login_required(login_url='login')
def agent_profile(request, pk):
    profile = request.user.profile.agents
    countries = Country.objects.all()

    if request.method == "POST":
        form  = AgentForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            instance = form.save(commit=False)
            old_instance = Agent.objects.get(user=profile.user.id)

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
        form = AgentForm(instance=profile)

    menu = 'user-management'
    s_menu = 'a-profile'
    
    context = {
        's_menu': s_menu,
        'menu': menu,
        'profile': profile,
        'form': form, 
        'countries': countries, 
    }
    return render(request, "agents/agent_profile.html", context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

@login_required(login_url='login')
def agentsDashboard(request, pk):
    menu = "agent-dashboard"
    context = {
        'username': pk,
        'menu': menu,
    }
    return render(request, "agents/A_dashboard.html", context)

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
    return render(request, "agents/view_connections.html", context)

@login_required(login_url='login')
def agent_properties(request, pk):
    menu = "agent-properties"
    s_menu = 'property-list'
    search_query = request.GET.get('search_query', '')
    if not search_query.isdigit() and search_query:
        houses = request.user.profile.agents.houses.filter(Q(address__icontains=search_query) |
                                                           Q(building_owner__building_owner_name__icontains=search_query) |
                                                           Q(occupancy_status__icontains=search_query))
    elif search_query.isdigit():
        houses = request.user.profile.agents.houses.filter(Q(house_number__icontains=search_query))
    else:
        houses = request.user.profile.agents.houses.all()

    context = {
        'menu': menu,
        'houses': houses,
        's_menu': s_menu,
        'search_query': search_query,
    }
    return render(request, "agents/agent_properties.html", context)

@login_required(login_url='login')
def agent_house_apartments(request, pk, house_id):
    menu = "agent-properties"
    s_menu = 'property-list'
    search_query = request.GET.get('search_query', '')
    house = request.user.profile.agents.houses.get(id=house_id)
    if not search_query.isdigit() and search_query:
        apartments = house.apartments.filter(Q(condition__icontains=search_query) |
                                             Q(is_occupied__iexact=search_query))
    elif search_query.isdigit():
        apartments = house.apartments.filter(Q(apartment_number__icontains=search_query) |
                                             Q(floor_number__icontains=search_query) |
                                             Q(number_of_rooms__icontains=search_query))
    else:
        apartments = house.apartments.all()
    context = {
        'menu': menu,
        'apartments': apartments,
        's_menu': s_menu,
        'house': house,
        'type': 'A',
        'search_query': search_query,
    }
    return render(request, "agents/agent_house_apartments.html", context)

@login_required(login_url='login')
def agent_house_apartment_details(request, pk, house_id, apartment_no):
    menu = "agent-properties"
    s_menu = 'property-list'
    house = request.user.profile.agents.houses.get(id=house_id)
    apartment = house.apartments.filter(apartment_number=apartment_no).first()
    
    context = {
        'menu': menu,
        'apartment': apartment,
        's_menu': s_menu,
        'house': house,
        'type': 'A',
    }
    return render(request, "agents/agent_house_apartment_details.html", context)