from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from notifications.models import Notification
from .models import WorkOrder
from .forms import  ServiceProviderForm
from .utils import paginateRequest


@login_required(login_url='login')
def requests(request, pk):
    i_menu = request.GET.get('i_menu', 'open')
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

    open = paginateRequest(request, sorted(open_requests, key=lambda x: x.reported_date, reverse=True), 5)
    in_progress = paginateRequest(request, sorted(in_progress_requests, key=lambda x: x.reported_date, reverse=True), 5)
    completed = paginateRequest(request, sorted(completed_requests, key=lambda x: x.reported_date, reverse=True), 5)
    closed = paginateRequest(request, sorted(closed_requests, key=lambda x: x.reported_date, reverse=True), 5)

    # for Notifications
    Notification.objects.filter(user=request.user).filter(status="UN", notification_type="MU").update(status="RD")
    
    context = {
        'menu': 'mt',
        's_menu': 'm-r',
        'open': open[1],
        'open_index': open[0],
        'in_progress': in_progress[1],
        'in_progress_index': in_progress[0],
        'completed': completed[1],
        'completed_index': completed[0],
        'closed': closed[1],
        'closed_index': closed[0],
        'open_count': len(open_requests),
        'in_progress_count': len(in_progress_requests),
        'completed_count': len(completed_requests),
        'closed_count': len(closed_requests),
        'i_menu': i_menu,
    }
    return render(request, 'building_owner_maintain/requests.html', context)

@login_required(login_url='login')
def cancel_request(request, pk):
    instance = WorkOrder.objects.get(id=pk)
    instance.status = 'closed'
    instance.reported_date =  timezone.now()
    instance.save()

    messages.success(request, f"Request with ID={pk} was cancelled.")
    return redirect("requests", pk=request.user.profile)

@login_required(login_url='login')
def reopen_request(request, pk):
    instance = WorkOrder.objects.get(id=pk)
    instance.status = 'open'
    instance.reported_date =  timezone.now()
    instance.assigned_to = None
    instance.save()

    messages.success(request, f"Request with ID={pk} was re-opened.")
    return redirect("requests", pk=request.user.profile)

@login_required(login_url='login')
def delete_request(request, pk):
    instance = WorkOrder.objects.get(id=pk)
    instance.delete()

    messages.success(request, f"Request with ID={pk} was deleted.")
    return redirect("requests", pk=request.user.profile)

@login_required(login_url='login')
def completed_request(request, pk):
    instance = WorkOrder.objects.get(id=pk)
    instance.status = 'completed'
    instance.reported_date =  timezone.now()
    instance.save()

    messages.success(request, f"Request with ID={pk} has been Completed.")
    return redirect("requests", pk=request.user.profile)

def assign_service_provider(request, pk, workorder_id):
    workorder = WorkOrder.objects.get(id=workorder_id)

    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            instance = form.save()

            workorder.assigned_to = instance
            workorder.status = 'in_progress'
            workorder.save()

            return redirect('requests', pk=request.user.profile)
    else:
        form = ServiceProviderForm()

    context = {
        'menu': 'mt',
        's_menu': 'm-s-p',
        'form': form,
    }
    return render(request,'building_owner_maintain/assign_service_provider.html', context)

def service_provider(request, pk, workorder_id):
    workorder = WorkOrder.objects.get(id=workorder_id)

    context = {
        'menu': 'mt',
        's_menu': 'm-s-p',
        'workorder': workorder,
        'sp': workorder.assigned_to,
    }
    return render(request,'building_owner_maintain/service_provider_details.html', context)