from django.shortcuts import render
from .models import Agent

def agentsDashboard(request, pk):
    active_menu = "agent-dashboard"
    context = {
        'username': pk,
        'active_menu': active_menu,
    }
    return render(request, "agents/A_dashboard.html", context)

