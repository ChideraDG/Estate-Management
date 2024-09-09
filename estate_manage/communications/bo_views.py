import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
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

    unread = 0
    for message in messages: 
        if message['unread'] > 0:
            unread += message['unread']

    context = {
        "menu": 'tm',
        "s_menu": 'ct',
        "tenants": tenants,
        "all_messages": messages,
        'unread_count': unread,
    }
    return render(request, 'communications/bo_comms.html', context)

def search_clients(request):
    query = request.GET.get('query', '')

    if ' ' in query:
        tenants = request.user.profile.building_owner.tenants.filter(Q(first_name__icontains=query.split(" ")[0].strip()) | 
                                                                     Q(last_name__icontains=query.split(" ")[1].strip()))
    elif query:
        tenants = request.user.profile.building_owner.tenants.filter(Q(first_name__icontains=query.strip()) | 
                                                                     Q(last_name__icontains=query.strip()))
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
