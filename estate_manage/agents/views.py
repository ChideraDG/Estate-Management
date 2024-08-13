from django.shortcuts import render

def agentsDashboard(request, pk):
    context = {'username': pk}
    return render(request, "agents/A_dashboard.html", context)

