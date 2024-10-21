from django.shortcuts import render


def request_submission(request, pk):
    context = {
        'menu': 'workorder',
        's_menu': 'rs',
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
