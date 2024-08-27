from django.shortcuts import render, redirect
from .forms import CompanyForm
from .models import Company
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='login')
def companyDashboard(request, pk):
    active_menu = 'company-dashboard'

    context = {
        'username': pk, 
        'active_menu': active_menu,
        }
    return render(request, "companies/C_dashboard.html", context)

@login_required(login_url='login')
def companyProfile(request, pk):
    try:
        profile = request.user.profile.companies
    except Company.DoesNotExist:
        return redirect('custom_404')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            instance = form.save(commit=False)  # Create a model instance but don't save it to the database yet.
            old_instance = Company.objects.get(user=profile.user.id)

            if instance.name:
                instance.name = instance.name.strip().title()
            
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
        form = CompanyForm(instance=profile)

    active_menu = 'user-management'
    active_sub_menu = 'c-profile'
        
    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
        'profile': profile,
        'form': form, 
        }
    return render(request, 'companies/company.html', context)

@login_required(login_url='login')
def view_connections(request, pk):
    active_menu = 'user-management'
    active_sub_menu = request.GET.get('active_sub_menu', 'personal-profile')

    context = {
        'active_sub_menu': active_sub_menu,
        'active_menu': active_menu,
    }
    return render(request, 'companies/viewConnections.html', context)
