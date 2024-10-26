from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import WorkOrder
from .forms import WorkOrderForm


@login_required(login_url='login')
def request_submission(request, pk):
    tenant = request.user.profile.tenant
    form = WorkOrderForm(tenant=tenant)

    if request.method == 'POST':
        form = WorkOrderForm(request.POST, tenant=tenant)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.apartment = tenant.apartment
            instance.save()
            messages.success(request, 'Work Order has been Logged')
            return redirect('log_request', pk=pk)
        else:
            print(form.errors)

    context = {
        'menu': 'workorder',
        's_menu': 'rs',
        'form': form,
    }
    return render(request, 'tenant_work_order/request_submission.html', context)

@login_required(login_url='login')
def tracking(request, pk):
    status = request.GET.get('status', 'all')
    workorder = WorkOrder.objects.filter(apartment__tenant_apartment__user=request.user.profile)
    
    open_request = workorder.filter(status='open')
    in_progress_request = workorder.filter(status='in_progress')
    completed_request = workorder.filter(status='completed')
    closed_request = workorder.filter(status='closed')

    context = {
        'menu': 'workorder',
        's_menu': 'tau',
        'open_count': open_request.count(),
        'in_progress_count': in_progress_request.count(),
        'completed_count': completed_request.count(),
        'closed_count': closed_request.count(),
        'open': open_request,
        'in_progress': in_progress_request,
        'completed': completed_request,
        'closed': closed_request,
        'workorder': workorder,
        'status': status,
    }

    return render(request, 'tenant_work_order/tracking.html', context)

@login_required(login_url='login')
def service_provider_details(request, pk):
    context = {
        'menu': 'workorder',
        's_menu': 'spi',
    }

    return render(request, 'tenant_work_order/service_provider.html', context)
