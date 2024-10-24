from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    context = {
        'menu': 'workorder',
        's_menu': 'tau',
    }

    return render(request, 'tenant_work_order/tracking.html', context)

@login_required(login_url='login')
def service_provider(request, pk):
    context = {
        'menu': 'workorder',
        's_menu': 'spi',
    }

    return render(request, 'tenant_work_order/service_provider.html', context)
