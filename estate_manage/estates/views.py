from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Estate, Photo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from locations.models import Country, State
from django.http import JsonResponse
from urllib.parse import urlencode
from .utils import paginateEstates

def deleteEstate(request, pk):
    profile = Estate.objects.get(id=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('home-estate')
    context = {'obj': profile}
    return render(request, 'estates/deleteEstate.html', context)



def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)

