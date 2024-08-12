from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from .models import Buyer
from .forms import BuyerForm

def buyerHome(request):
    profile = Buyer.objects.all()
    context = {'profile': profile}
    return render(request, 'buyers/buyerHome.html', context)

def createBuyer(request):
    countries = Country.objects.all()
    form = BuyerForm()

    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES)
        if form.is_valid():
            buyer = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            if buyer.full_name:
                buyer.full_name = buyer.full_name.strip().title()
            buyer.save()
            return redirect('buyer-home')

    context = {'form': form, 'countries': countries}
    return render(request, 'buyers/buyerReg.html', context)

def updateBuyer(request, pk):
    pass

def viewBuyer(request, pk):
    pass

def deleteBuyer(request, pk):
    pass

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
    



