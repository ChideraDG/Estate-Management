from django.shortcuts import render, redirect
from .models import Tenant
from .forms import TenantForm
from django.http import JsonResponse
from locations.models import Country, State


def tenantHome(request):
    profiles = Tenant.objects.all()
    context = {'profiles': profiles}
    return render(request, 'tenants/tenantHome.html', context)

def createTenant(request):
    countries = Country.objects.all()
    form = TenantForm()

    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            
            if instance.first_name:
                instance.first_name = instance.first_name.strip().title()
            if instance.last_name:
                instance.last_name = instance.last_name.strip().title()
            if instance.emergency_contact_name:
                instance.emergency_contact_name = instance.emergency_contact_name.strip().title()
            instance.save()
            return redirect('tenant-home')
        
    context = {'form': form, 'countries': countries}
    return render(request, 'tenants/tenantReg.html', context)

def updateTenant(request, pk):
    countries = Country.objects.all()
    profile = Tenant.objects.get(id=pk)
    form = TenantForm(instance=profile)

    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
           
            if instance.first_name:
                instance.first_name = instance.first_name.strip().title()
            if instance.last_name:
                instance.last_name = instance.last_name.strip().title()
            if instance.emergency_contact_name:
                instance.emergency_contact_name = instance.emergency_contact_name.strip().title()
            instance.save()
            return redirect('tenant-home')
        
    context = {'form': form, 'profile': profile, 'countries': countries}
    return render(request, 'tenants/tenantReg.html', context)

def viewTenant(request, pk):
    tenant = Tenant.objects.get(id=pk)
    context = {'tenant': tenant}
    return render(request, 'tenants/viewTenant.html', context)

def deleteTenant(request, pk):
    profile = Tenant.objects.get(id=pk)

    if request.method == 'POST':
        profile.delete()
        return redirect('tenant-home')
    
    context = {'obj': profile}
    return render(request, 'tenants/deleteTenant.html', context)

def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
    

