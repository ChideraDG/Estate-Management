from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from .models import Buyer
from .forms import BuyerForm

def buyerHome(request):
    profiles = Buyer.objects.all()
    context = {'profiles': profiles}
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
    countries = Country.objects.all()
    profile = Buyer.objects.get(id=pk)
    form = BuyerForm(instance=profile)


    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            buyer = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            if buyer.full_name:
                buyer.full_name = buyer.full_name.strip().title()
            buyer.save()
            return redirect('buyer-home')

    context = {'form': form, 'countries': countries, 'profile':profile}
    return render(request, 'buyers/buyerReg.html', context)

def viewBuyer(request, pk):
    buyer = Buyer.objects.get(id=pk)
    context = {'buyer': buyer}
    return render(request, 'buyers/viewBuyer.html', context)

def deleteBuyer(request, pk):
    profile = Buyer.objects.get(id=pk)

    if request.method == 'POST':
        profile.delete()
        return redirect('buyer-home')
    
    context = {'obj': profile}
    return render(request, 'buyers/deleteBuyer.html', context)

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
    
def buyerDashboard(request, pk):
    context = {'username': pk}
    return render(request, "buyers/B_dashboard.html", context)


