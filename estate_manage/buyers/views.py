from django.shortcuts import render, redirect
from locations.models import Country, State
from django.http import JsonResponse
from .models import Buyer
from .forms import BuyerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def buyerProfile(request,pk):
    try:
        profile = request.user.profile.buyers
    except Buyer.DoesNotExist:
        return redirect('custom_404')

    if request.method == 'POST':
        form = BuyerForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            old_instance = Buyer.objects.get(user=profile.user.id)

            if instance.full_name:
                instance.full_name = instance.full_name.strip().title()
            
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
        form = BuyerForm(instance=profile)

    menu = 'user-management'
    s_menu = 'b-profile'
        
    context = {
        's_menu': s_menu,
        'menu': menu,
        'profile': profile,
        'form': form, 
        }

    return render(request, 'buyers/buyer.html', context)

@login_required(login_url='login')
def get_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    states_list = [{'id': state.id, 'name': state.name} for state in states]
    return JsonResponse(states_list, safe=False)
    
@login_required(login_url='login')
def buyerDashboard(request, pk):
    menu = 'buyer-dashboard'

    context = {
        'username': pk, 
        'menu': menu,
        }
    return render(request, "buyers/B_dashboard.html", context)

@login_required(login_url='login')
def view_connections(request, pk):
    menu = 'user-management'
    s_menu = request.GET.get('s_menu', 'personal-profile')

    context = {
        's_menu': s_menu,
        'menu': menu,
    }
    return render(request, 'buyers/viewConnections.html', context)


