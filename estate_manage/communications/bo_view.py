import datetime
import time
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from building_owners.models import BuildingOwner
from users.models import Profile
from .models import Message


def bo_tenant_communications(request, pk):
    tenants = request.user.profile.building_owner.tenants.all()

    # Prepare a list to hold message data
    messages = []

    # Iterate over tenants
    for tenant in tenants:
        # Prepare a query to fetch relevant messages
        messages_queryset = Message.objects.filter(
            Q(sender=request.user, recipient=tenant.user.user) |
            Q(sender=tenant.user.user, recipient=request.user)
        )
        
        if messages_queryset.exists():
            # Get the latest message
            latest_message = messages_queryset.last()
            
            # Prepare the message data
            message_data = {
                'id': tenant.id,
                'profile_picture': tenant.profile_picture,
                'name': f"{tenant.first_name} {tenant.last_name}",
                'latest_message': latest_message.message,
                'unread': messages_queryset.filter(recipient=request.user, is_read=False).count(),
                'read': latest_message.is_read,
                'timestamp': latest_message.timestamp,
            }
            
            # Append to the list
            messages.append(message_data)

    # Sort the list by timestamp (already sorted by queryset, but keeping this for extra safety)
    messages = sorted(messages, key=lambda x: x['timestamp'], reverse=True)

    # The total unread messages across all tenants
    unread_total = bo_get_unread(request)
    Profile.objects.filter(username=request.user).update(unread_messages=unread_total)

    # To count the unread messages for each tenant individually
    unread = sum(message['unread'] for message in messages)

    context = {
        "menu": 'tm',
        "s_menu": 'ct',
        "tenants": tenants,
        "all_messages": messages,
        'unread_count': unread,
        'unread_total': unread_total,
    }
    return render(request, 'communications/bo_comms.html', context)

def search_clients(request):
    query = request.GET.get('query', '').strip()

    if ' ' in query:
        tenants = request.user.profile.building_owner.tenants.filter(Q(first_name__icontains=query.split(" ")[0]) | 
                                                                     Q(last_name__icontains=query.split(" ")[1]))
    elif query:
        tenants = request.user.profile.building_owner.tenants.filter(Q(first_name__icontains=query) | 
                                                                     Q(last_name__icontains=query))
    else:
        tenants = request.user.profile.building_owner.tenants.all()
 
    results = [
        {
            'id': tenant.id,
            'first_name': tenant.first_name,
            'last_name': tenant.last_name,
            'profile_picture': tenant.profile_picture.url,
            'house_number': tenant.house.house_number,
            'address': tenant.house.address,
            'url': reverse('bo-chat', kwargs={'pk': request.user.profile, 'tenant_id': tenant.id}),
        }
        for tenant in tenants
    ]
    return JsonResponse({'clients': results}, safe=False)

def search_chats(request):
    query = request.GET.get('query', '').strip()
    user_profile = request.user.profile

    # Filter tenants based on the search query
    if ' ' in query:
        tenants = request.user.profile.building_owner.tenants.filter(Q(first_name__icontains=query.split(" ")[0]) | 
                                                                     Q(last_name__icontains=query.split(" ")[1]))
    elif query:
        tenants = request.user.profile.building_owner.tenants.filter(Q(first_name__icontains=query) | 
                                                                     Q(last_name__icontains=query))
    else:
        tenants = request.user.profile.building_owner.tenants.all()

    # Prepare chat data to return in JSON format
    chat_data = []
    for tenant in tenants:
        # Fetch the latest message between the user and tenant
        latest_message = Message.objects.filter(
            Q(sender=request.user, recipient=tenant.user.user) |
            Q(sender=tenant.user.user, recipient=request.user)
        ).last()

        if latest_message:
            chat_data.append({
                'url': reverse('bo-chat', kwargs={'pk': request.user.profile, 'tenant_id': tenant.id}),
                'profile_picture': tenant.profile_picture.url,
                'name': f"{tenant.first_name} {tenant.last_name}",
                'latest_message': latest_message.message[:30],  # Truncate message
                'timestamp': latest_message.timestamp.strftime("%b %d, %H:%M"),
                'unread': Message.objects.filter(recipient=request.user, sender=tenant.user.user, is_read=False).count(),
            })

    chat_data = sorted(chat_data, key=lambda x: x['timestamp'], reverse=True)
    return JsonResponse({'chats': chat_data})

def bo_chat(request, pk, tenant_id):
    tenant = request.user.profile.building_owner.tenants.get(id=tenant_id)
    messages = Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                      Q(sender=tenant.user.user, recipient=request.user))
    
    # Group messages by date
    messages_by_date = {}
    for message in messages:
        message_date = message.timestamp.date()
        if message_date not in messages_by_date:
            messages_by_date[message_date] = []
        messages_by_date[message_date].append(message)
        
    if messages:
        if messages.last().recipient == request.user:
            read = messages.filter(is_read=False)
            read.update(is_read=True)
            
    Profile.objects.filter(username=request.user).update(unread_messages=bo_get_unread(request))

    if request.method == "POST":
        message_content = request.POST.get("message", "").strip()

        if message_content:  # Ensure message isn't empty
            Message.objects.create(
                sender=request.user,
                recipient=tenant.user.user,
                message=message_content
            )

            return redirect("bo-chat", pk=request.user.profile, tenant_id=tenant_id)
    
    context = {
        "menu": 'tm',
        "s_menu": 'ct',
        "tenant": tenant,
        'messages_by_date': messages_by_date,
        'today_date': datetime.date.today(),
    }
    return render(request, "communications/bo_chat.html", context)

def bo_get_unread(request):
    tenants = request.user.profile.building_owner.tenants.all()

    # Prepare a list to hold the unread counts
    unread_total = []

    # Iterate over tenants
    for tenant in tenants:
        # Query for unread messages sent to the current user from each tenant
        unread_count = Message.objects.filter(
            sender=tenant.user.user, 
            recipient=request.user, 
            is_read=False
        ).count()

        if unread_count > 0:
            unread_total.append(unread_count)

    return len(unread_total)
