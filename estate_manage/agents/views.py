from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Agent


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