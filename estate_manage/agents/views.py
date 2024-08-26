from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from locations.models import Country, State
from .models import Agent
from  .forms import AgentForm


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

    active_menu = 'user-management'
    active_sub_menu = 'a-profile'
    
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
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
    active_menu = "agent-dashboard"
    context = {
        'username': pk,
        'active_menu': active_menu,
    }
    return render(request, "agents/A_dashboard.html", context)

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
    return render(request, "agents/view_connections.html", context)