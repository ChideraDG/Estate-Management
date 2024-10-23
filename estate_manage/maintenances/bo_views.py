from django.shortcuts import render, redirect
from django.contrib import messages
from .models import WorkOrder


def requests(request, pk):
    section = request.GET.get('section', '')
    tenants = request.user.profile.building_owner.tenants.all()
    open_requests, in_progress_requests, completed_requests, closed_requests = [], [], [], []

    for tenant in tenants:
        if tenant.apartment.work_orders.exists():
            for log in tenant.apartment.work_orders.all():
                if log.status == 'open':
                    open_requests.append(log)
                elif log.status == 'in_progress':
                    in_progress_requests.append(log)
                elif log.status == 'completed':
                    completed_requests.append(log)
                elif log.status == 'closed':
                    closed_requests.append(log)
    
    context = {
        'menu': 'mt',
        's_menu': 'm-r',
        'open': sorted(open_requests, key=lambda x: x.reported_date, reverse=True),
        'in_progress': sorted(in_progress_requests, key=lambda x: x.reported_date, reverse=True),
        'completed': sorted(completed_requests, key=lambda x: x.reported_date, reverse=True),
        'closed': sorted(closed_requests, key=lambda x: x.reported_date, reverse=True),
        'open_count': len(open_requests),
        'in_progress_count': len(in_progress_requests),
        'completed_count': len(completed_requests),
        'closed_count': len(closed_requests),
        'section': section,
    }
    return render(request, 'building_owner_maintain/requests.html', context)