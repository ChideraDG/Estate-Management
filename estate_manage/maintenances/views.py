from django.shortcuts import render
from .forms import WorkOrderForm


def request_submission(request, pk):
    tenant = request.user.profile.tenant
    form = WorkOrderForm(tenant=tenant)

    if request.method == 'POST':
        form = WorkOrderForm(request.POST, tenant=tenant)

        if form.is_valid():
            form.save()

    context = {
        'menu': 'workorder',
        's_menu': 'rs',
        'form': form,
    }
    return render(request, 'tenant_work_order/request_submission.html', context)

def tracking(request, pk):
    context = {
        'menu': 'workorder',
        's_menu': 'tau',
    }

    return render(request, 'tenant_work_order/tracking.html', context)

def service_provider(request, pk):
    context = {
        'menu': 'workorder',
        's_menu': 'spi',
    }

    return render(request, 'tenant_work_order/service_provider.html', context)
