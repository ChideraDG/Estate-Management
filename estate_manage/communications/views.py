from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from .models import Message


def bo_tenant_communications(request, pk):
    tenants = request.user.profile.building_owner.tenants.all()
    messages = [
        {
            'id': tenant.id,
            'profile_picture': tenant.profile_picture,
            'name': tenant.first_name + " " + tenant.last_name,
            'latest_message': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                     Q(sender=tenant.user.user, recipient=request.user)).last().message,
            'unread': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                             Q(sender=tenant.user.user, recipient=request.user)).filter(recipient=request.user, is_read=False),
            'read': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                           Q(sender=tenant.user.user, recipient=request.user)).last().is_read,
            'timestamp': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                Q(sender=tenant.user.user, recipient=request.user)).last().timestamp,
        }
        for tenant in tenants if Message.objects.filter(Q(recipient=tenant.user.user) | 
                                                        Q(sender=tenant.user.user)).exists()
    ]
    
    unread_messages = [
        {
            'id': tenant.id,
            'profile_picture': tenant.profile_picture,
            'name': tenant.first_name + " " + tenant.last_name,
            'latest_message': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                        Q(sender=tenant.user.user, recipient=request.user)).filter(is_read=False).last().message,
            'unread': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                Q(sender=tenant.user.user, recipient=request.user)).filter(recipient=request.user, is_read=False),
            'read': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                            Q(sender=tenant.user.user, recipient=request.user)).filter(is_read=False).last().is_read,
            'timestamp': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                Q(sender=tenant.user.user, recipient=request.user)).filter(is_read=False).last().timestamp,
        }
        for tenant in tenants if Message.objects.filter(Q(recipient=tenant.user.user) | 
                                                    Q(sender=tenant.user.user)).filter(is_read=False).exists()
    ]

    read_messages = [
        {
            'id': tenant.id,
            'profile_picture': tenant.profile_picture,
            'name': tenant.first_name + " " + tenant.last_name,
            'latest_message': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                        Q(sender=tenant.user.user, recipient=request.user)).filter(is_read=True).last().message,
            'unread': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                Q(sender=tenant.user.user, recipient=request.user)).filter(recipient=request.user, is_read=True),
            'read': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                            Q(sender=tenant.user.user, recipient=request.user)).filter(is_read=True).last().is_read,
            'timestamp': Message.objects.filter(Q(sender=request.user, recipient=tenant.user.user) |
                                                Q(sender=tenant.user.user, recipient=request.user)).filter(is_read=True).last().timestamp,
        }
        for tenant in tenants if Message.objects.filter(Q(recipient=tenant.user.user) | 
                                                    Q(sender=tenant.user.user)).filter(is_read=True).exists()
    ]
    print(len(read_messages))
    context = {
        "menu": 'tm',
        "s_menu": 'ct',
        "tenants": tenants,
        "all_messages": messages,
        "unread_messages": unread_messages,
        "read_messages": read_messages
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

    context = {
        "menu": 'tm',
        "s_menu": 'ct',
        "tenant": tenant,
        "all_messages": messages
    }
    return render(request, "communications/bo_chat.html", context)
